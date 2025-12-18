from odoo import models, fields

class rental_pricing(models.Model):
    _name = 'rental.pricing'
    _description = 'Règle tarifaire de location'

    category_id = fields.Many2one('product.category', string="Catégorie de vélo")
    billing_unit = fields.Selection([
        ('hour', 'Heure'),
        ('day', 'Jour'),
        ('month', 'Mois'),
    ], default='day')
    price = fields.Float("Prix unitaire")
    active = fields.Boolean(default=True)
    vip_price = fields.Boolean(default=False)