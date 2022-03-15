from ast import literal_eval

from odoo import models, fields, api


class ProductBom(models.TransientModel):
    _inherit = "res.config.settings"

    product_ids = fields.Many2many('product.template', string="product")

    def set_values(self):
        res = super(ProductBom, self).set_values()
        self.env['ir.config_parameter'].set_param('bom_in_cart.product_ids', self.product_ids.ids)
        return res

    @api.model
    def get_values(self):
        res = super(ProductBom, self).get_values()
        product_ids = self.env['ir.config_parameter'].sudo().get_param('bom_in_cart.product_ids')
        print("product_ids", product_ids)
        res.update(product_ids=[(6, 0, literal_eval(product_ids))]
                   )
        print("TEST", type(literal_eval(product_ids)))
        return res
