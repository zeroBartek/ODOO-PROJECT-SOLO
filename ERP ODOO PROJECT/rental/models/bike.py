from odoo import models, fields

class bike(models.Model):
    _inherit = 'product.template'

    for_rent = fields.Boolean(default=False)
    size = fields.Char("Taille S,M ou L")
    couleur = fields.Char("Couleur du vélo")
    condition = fields.Selection([
        ('new', 'Neuf'),
        ('reconditionned', 'reconditionné'),
        ('damaged', 'Endommagé'),
    ], default='new')
    rental_status = fields.Selection([
        ('available', 'Disponible'),
        ('rented', 'Loué'),
        ('maintenance', 'En maintenance'),
    ], default='available')