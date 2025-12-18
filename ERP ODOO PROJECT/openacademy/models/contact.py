from odoo import models, fields, api


class openacademy_contact(models.Model):
    _name = 'openacademy.contact'
    _description = 'openacademy.contact'

    name = fields.Char()
    photo = fields.Binary()
    birth_date = fields.Date()
    age = fields.Integer(compute="_age_compute")
    email = fields.Char()
    phone = fields.Char()

    @api.depends("birth_date")
    def _age_compute(self):
        for record in self:
            if record.birth_date:
                record.age = (fields.Date.today() - record.birth_date).days / 365
            else:
                record.age = 0

    @api.onchange('birthday_date')
    def _onchange_age_limit(self):
        if self.age<18:
            return {'warning':{'title','etc etc etc'}}
    
    #sessions = fields.One2many('openacademy.session','participants')
    
    
    


