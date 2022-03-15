from odoo import models, fields


class TravelService(models.Model):
    _name = "travel.service"
    _description = "Travel service"
    _rec_name = "service"

    service = fields.Char('Service Type', required=True)
    expiration_period = fields.Integer('Expiration Period', required=True, )
