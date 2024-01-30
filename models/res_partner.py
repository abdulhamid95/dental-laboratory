from odoo import fields, models, api


class res_partner_inherit(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _description = 'this module update partner form'


    doctor_code = fields.Char("Doctor Code")