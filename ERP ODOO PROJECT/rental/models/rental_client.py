from odoo import models, fields, api

class rental_client(models.Model):
    _inherit = 'res.partner'

    is_rental_client = fields.Boolean(string="Client de location", default=False)
    is_vip = fields.Boolean(string='Client VIP')
    total_contracts = fields.Integer(string='Nombre de contrats', compute='_compute_total_contracts')
    contract_ids = fields.One2many('rental.contract', 'client_id', string='Contrats de location')

    @api.depends('contract_ids')
    def _compute_total_contracts(self):
        for rec in self:
            rec.total_contracts = len(rec.contract_ids)
