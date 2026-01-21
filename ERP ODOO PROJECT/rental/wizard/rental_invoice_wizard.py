from odoo import models, fields
from odoo.exceptions import UserError


class rental_invoice_wizard(models.TransientModel):
    _name = 'rental.invoice.wizard'
    _description = 'Wizard facture contrat de location'

    contract_id = fields.Many2one(
        'rental.contract',
        string="Contrat",
        required=True,
        readonly=True,
        default=lambda self: self.env.context.get('active_id')
    )

    invoice_date = fields.Date(string="Date facture", default=fields.Date.context_today)
    journal_id = fields.Many2one('account.journal', string="Journal", domain=[('type', '=', 'sale')])
    invoice_payment_term_id = fields.Many2one('account.payment.term', string="Conditions de paiement")
    invoice_user_id = fields.Many2one('res.users', string="Commercial")
    notes = fields.Text(string="Notes / Conditions")

    fee = fields.Monetary(string="Frais supplémentaire", default=0.0)
    fee_label = fields.Char(string="Libellé frais", default="Frais supplémentaire")
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    def action_create_invoice(self):
        self.ensure_one()

        if not self.contract_id:
            raise UserError("Aucun contrat trouvé (active_id manquant).")
        if self.contract_id.invoice_id:
            raise UserError("Une facture existe déjà pour ce contrat.")

        invoice = self.contract_id._create_invoice()

        vals = {}
        if self.invoice_date:
            vals['invoice_date'] = self.invoice_date
        if self.journal_id:
            vals['journal_id'] = self.journal_id.id
        if self.invoice_payment_term_id:
            vals['invoice_payment_term_id'] = self.invoice_payment_term_id.id
        if self.invoice_user_id:
            vals['invoice_user_id'] = self.invoice_user_id.id
        if self.notes:
            vals['notes'] = self.notes
        if vals:
            invoice.write(vals)

        if self.fee and self.fee > 0:
            invoice.write({
                'invoice_line_ids': [(0, 0, {
                    'name': self.fee_label or 'Frais supplémentaire',
                    'quantity': 1.0,
                    'price_unit': self.fee,
                })]
            })

        self.contract_id.state = 'done'

        return {
            'type': 'ir.actions.act_window',
            'name': 'Facture',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
        }
