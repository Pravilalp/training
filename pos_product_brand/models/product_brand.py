from odoo import models, fields


class PosBrand(models.Model):
    _inherit = 'product.product'

    brand_id = fields.Many2one('product.brand', string="Brand")


class ProductBrand(models.Model):
    _name = 'product.brand'

    name = fields.Char(string="Brand Name")
