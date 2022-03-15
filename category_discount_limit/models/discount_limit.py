from odoo import models, fields, api


class DiscountLimit(models.Model):
    _inherit = "pos.config"

    discount_limit = fields.Boolean(string="Apply Discount Limit")

    @api.onchange('discount_limit')
    def onchange_discount_limit(self):
        categories = self.env['pos.category'].search([])
        if self.discount_limit == True:
            for category in categories:
                category.apply_limit = True
        else:
            for category in categories:
                category.apply_limit = False


class ProductCategory(models.Model):
    _inherit = "pos.category"

    discount = fields.Char(string="Discount Limit(%)")
    apply_limit = fields.Boolean()


class PosSession(models.Model):
    _inherit = "pos.session"

    limit_discount = fields.Boolean(string="Discount Limit")
