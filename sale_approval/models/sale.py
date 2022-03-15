from odoo import models, fields, api, _


# from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('to_approve', 'Waiting for Approval'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    user_check = fields.Boolean(string="user check", compute='_compute_user_check')
    price_check = fields.Boolean(string="price check")
    approve_check = fields.Boolean(string="approve check")
    submit_check = fields.Boolean(string="manager button", )

    @api.depends('partner_id')
    def _compute_user_check(self):
        self.user_check = False
        for rec in self:
            # rec.user_check = False
            print(self.env.user)
            flag = self.env.user.has_group('sales_team.group_sale_manager')
            print(flag)
            if not flag:
                rec.user_check = True

    @api.onchange('order_line')
    def _onchange_unit_price(self):
        if self.order_line:
            for rec in self.order_line:
                price = rec.product_id.list_price
                line_price = rec.price_unit
                self.price_check = False
                flag = self.env.user.has_group('sales_team.group_sale_manager')
                print(flag)
                if not flag:
                    if price != line_price:
                        return {'warning': {
                            'title': _("Warning"),
                            'message': _(
                                "Need Approval From Manager, Unit price From Sale Order Line Is Differnt From Product Sales Price.")
                        }}

    def action_quotation_send(self):
        flag = self.env.user.has_group('sales_team.group_sale_manager')
        if flag:
            attrs = super(SaleOrder, self).action_quotation_send()
            return attrs
        else:
            if self.approve_check:
                attrs = super(SaleOrder, self).action_quotation_send()
                return attrs
            for rec in self.order_line:
                print(rec.product_id)
                price = rec.product_id.list_price
                line_price = rec.price_unit
                self.price_check = False
                if price != line_price:
                    self.price_check = True
                    break
                else:
                    self.price_check = False
            if self.price_check != True:
                attrs = super(SaleOrder, self).action_quotation_send()
                return attrs

    def action_confirm(self):
        flag = self.env.user.has_group('sales_team.group_sale_manager')
        if flag:
            attrs = super(SaleOrder, self).action_confirm()
            return attrs
        else:
            if self.approve_check:
                attrs = super(SaleOrder, self).action_confirm()
                return attrs
            for rec in self.order_line:
                print(rec.product_id)
                price = rec.product_id.list_price
                line_price = rec.price_unit
                self.price_check = False
                if price != line_price:
                    self.price_check = True
                    break
                else:
                    self.price_check = False
            if self.price_check != True:
                attrs = super(SaleOrder, self).action_confirm()
                return attrs

    def action_approve(self):
        self.state = 'sent'
        self.approve_check = True

    def action_disapprove(self):
        self.state = 'draft'

    def manager_submit(self):
        self.state = 'to_approve'
