from odoo import models, fields, api
from odoo.exceptions import UserError


class rental_contract(models.Model):
    _name = 'rental.contract'
    _description = 'Contrat de location de vélo'

    client_id = fields.Many2one(
        'res.partner',
        string="Client",
        required=True,
        domain=[('is_rental_client', '=', True)]
    )
    bike_id = fields.Many2one(
        'product.template',
        string="Vélo",
        required=True,
        domain=[
            ('for_rent', '=', True),
            ('rental_status', '=', 'available'),
            ('condition', '!=', 'damaged'),
        ]
    )
    pricing_id = fields.Many2one(
        'rental.pricing',
        string="Règle tarifaire",
        compute='_compute_pricing',
        store=True
    )
    date_start = fields.Datetime(required=True, string="Début")
    date_end = fields.Datetime(required=True, string="Fin")
    billing_unit = fields.Selection(
        [('hour', 'Heure'), ('day', 'Jour'), ('month', 'Mois')],
        default='day',
        string="Unité de facturation"
    )
    price_unit = fields.Float(string="Prix unitaire", compute='_compute_price_unit', store=True)
    amount_total = fields.Monetary(string="Total", compute="_compute_amount_total", store=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    state = fields.Selection(
        [
            ('draft', 'Brouillon'),
            ('confirmed', 'Confirmé'),
            ('ongoing', 'En cours'),
            ('done', 'Terminé'),
            ('Cancelled', 'Annulé'),
        ],
        default='draft'
    )
    invoice_id = fields.Many2one('account.move', string="Facture", readonly=True, copy=False)

    rental_count_month = fields.Integer(
        string="Nb de locations ce mois",
        compute="_compute_bike_stats_month",
        store=False
    )

    rental_income_month = fields.Monetary(
        string="Revenu du vélo ce mois",
        compute="_compute_bike_stats_month",
        currency_field='currency_id',
        store=False
    )

    @api.depends('bike_id', 'billing_unit', 'client_id.is_vip')
    def _compute_pricing(self):
        for rec in self:
            if rec.bike_id and rec.bike_id.categ_id:
                rec.pricing_id = self.env['rental.pricing'].search([
                    ('category_id', '=', rec.bike_id.categ_id.id),
                    ('billing_unit', '=', rec.billing_unit),
                    ('vip_price', '=', bool(rec.client_id and rec.client_id.is_vip))
                ], limit=1)
            else:
                rec.pricing_id = False

    @api.depends('pricing_id')
    def _compute_price_unit(self):
        for rec in self:
            rec.price_unit = rec.pricing_id.price if rec.pricing_id else 0.0

    @api.depends('date_start', 'date_end', 'price_unit', 'billing_unit')
    def _compute_amount_total(self):
        for rec in self:
            if rec.date_start and rec.date_end:
                delta = rec.date_end - rec.date_start
                if rec.billing_unit == 'hour':
                    qty = delta.total_seconds() / 3600
                elif rec.billing_unit == 'day':
                    qty = max(delta.days, 1)
                else:
                    qty = delta.days / 30
                rec.amount_total = rec.price_unit * qty
            else:
                rec.amount_total = 0

    def action_confirm(self):
        for rec in self:
            rec._create_invoice()
            rec.state = 'confirmed'

    def action_start(self):
        self.state = 'ongoing'

    def action_close(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'Cancelled'

    def _create_invoice(self):
        Account = self.env['account.account']
        Journal = self.env['account.journal']

        for rec in self:
            if rec.invoice_id:
                return rec.invoice_id

            line_vals = {
                'name': f"Location vélo : {rec.bike_id.name} du {rec.date_start} au {rec.date_end}",
                'quantity': 1.0,
                'price_unit': rec.amount_total,
            }

            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': rec.client_id.id,
                'invoice_origin': f"Contrat de location {rec.id}",
                'invoice_line_ids': [(0, 0, line_vals)],
            }

            invoice = self.env['account.move'].create(invoice_vals)
            rec.invoice_id = invoice.id
            return invoice

    def open_invoice(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Facture',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.invoice_id.id,
        }

    @api.depends('bike_id', 'state', 'date_start', 'amount_total')
    def _compute_bike_stats_month(self):
        today = fields.Date.context_today(self)
        month = today.month
        year = today.year

        Contract = self.env['rental.contract']
        for rec in self:
            rec.rental_count_month = 0
            rec.rental_income_month = 0.0

            if not rec.bike_id:
                continue

            bike_contracts = Contract.search([
                ('state', '=', 'done'),
                ('bike_id', '=', rec.bike_id.id),
            ])

            for c in bike_contracts:
                if c.date_start:
                    ds = c.date_start.date()

                    if ds.month == month and ds.year == year:
                        rec.rental_count_month += 1
                        rec.rental_income_month += c.amount_total

            
