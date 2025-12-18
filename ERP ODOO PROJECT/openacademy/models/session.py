from odoo import models, fields


class openacademy_session(models.Model):
    _name = 'openacademy.session'
    _description = 'openacademy.session'

    name = fields.Char(required=True)
    contact_ids = fields.Many2many('openacademy.contact')
    course_id = fields.Many2one("openacademy.course",string="Course")
    max_participants = fields.Integer()
    
    date_start = fields.Date()
    date_end = fields.Date()
    duration=fields.Integer()
    attendee_ids = fields.Many2many("openacademy.contact","session_contact_rel", string="Attendees")
    
    



