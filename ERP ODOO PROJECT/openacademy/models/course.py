from odoo import models, fields, api


class openacademy_course(models.Model):
    _name = 'openacademy.course'
    _description = 'openacademy.course'

    name = fields.Char()
    description = fields.Text()
    session_ids = fields.One2many('openacademy.session','course_id')
    level = fields.Selection([('easy','Easy'), ('middle','Middle'),('hard','Hard')])
    
     #sessions = fields.One2many('openacademy.session','cours')
    #responsable_du_cours = fields.Many2one('openacademy.contact')
    


