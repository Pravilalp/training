from ast import literal_eval

from werkzeug.exceptions import NotFound

from odoo import http, fields
from odoo.http import request
from odoo.tools.json import scriptsafe as json_scriptsafe


class WebsiteSale(http.Controller):

    @http.route(['/shop/cart'], type='http', auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive='', **post):

        """
        Main cart management + abandoned cart revival
        access_token: Abandoned cart SO access token
        revive: Revival method when abandoned cart. Can be 'merge' or 'squash'
        """
        order = request.website.sale_get_order()

        "*******************************Bill of Material in cart*****************************************"
        product_ids = request.env['ir.config_parameter'].sudo().get_param('bom_in_cart.product_ids')
        bom = request.env['mrp.bom'].sudo().search([])
        list = []
        for i in bom.product_tmpl_id.ids:
            for j in literal_eval(product_ids):
                if i == j:
                    for a in order.order_line:
                        if i == a.product_id.product_tmpl_id.id:
                            # print(i)
                            list.append(i)
        print('list', list)
        line = []
        for p in list:
            print(p)
            bo = request.env['mrp.bom'].sudo().search([('product_tmpl_id', '=', p)])
            line.append(bo)
        "************************************************************************************************"

        if order and order.state != 'draft':
            request.session['sale_order_id'] = None
            order = request.website.sale_get_order()

        values = {}

        if access_token:
            abandoned_order = request.env['sale.order'].sudo().search([('access_token', '=', access_token)], limit=1)
            if not abandoned_order:  # wrong token (or SO has been deleted)
                raise NotFound()
            if abandoned_order.state != 'draft':  # abandoned cart already finished
                values.update({'abandoned_proceed': True})
            elif revive == 'squash' or (revive == 'merge' and not request.session.get(
                    'sale_order_id')):  # restore old cart or merge with unexistant
                request.session['sale_order_id'] = abandoned_order.id
                return request.redirect('/shop/cart')
            elif revive == 'merge':
                abandoned_order.order_line.write({'order_id': request.session['sale_order_id']})
                abandoned_order.action_cancel()
            elif abandoned_order.id != request.session.get(
                    'sale_order_id'):  # abandoned cart found, user have to choose what to do
                values.update({'access_token': abandoned_order.access_token})

        values.update({
            'website_sale_order': order,
            'date': fields.Date.today(),
            'suggested_products': [],
            'bom_products': line,

        })

        if order:
            order.order_line.filtered(lambda l: not l.product_id.active).unlink()
            _order = order
            if not request.env.context.get('pricelist'):
                _order = order.with_context(pricelist=order.pricelist_id.id)
            values['suggested_products'] = _order._cart_accessories()

        if post.get('type') == 'popover':
            # force no-cache so IE11 doesn't cache this XHR
            return request.render("website_sale.cart_popover", values, headers={'Cache-Control': 'no-cache'})

        return request.render("website_sale.cart", values)

    @http.route(['/shop/cart/update_json'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True, **kw):
        print("****************quantity***************")
        """
        This route is called :
            - When changing quantity from the cart.
            - When adding a product from the wishlist.
            - When adding a product to cart on the same page (without redirection).
        """

        order = request.website.sale_get_order(force_create=1)
        if order.state != 'draft':
            request.website.sale_reset()
            if kw.get('force_create'):
                order = request.website.sale_get_order(force_create=1)
            else:
                return {}
        "*******************************Bill of Material in cart*****************************************"
        product_ids = request.env['ir.config_parameter'].sudo().get_param('bom_in_cart.product_ids')
        bom = request.env['mrp.bom'].sudo().search([])
        list = []
        for i in bom.product_tmpl_id.ids:
            for j in literal_eval(product_ids):
                if i == j:
                    for a in order.order_line:
                        if i == a.product_id.product_tmpl_id.id:
                            # print(i)
                            list.append(i)
        print('list', list)
        line = []
        for p in list:
            print(p)
            bo = request.env['mrp.bom'].sudo().search([('product_tmpl_id', '=', p)])
            line.append(bo)
        "************************************************************************************************"

        pcav = kw.get('product_custom_attribute_values')
        nvav = kw.get('no_variant_attribute_values')
        value = order._cart_update(
            product_id=product_id,
            line_id=line_id,
            add_qty=add_qty,
            set_qty=set_qty,
            product_custom_attribute_values=json_scriptsafe.loads(pcav) if pcav else None,
            no_variant_attribute_values=json_scriptsafe.loads(nvav) if nvav else None,

        )
        if not order.cart_quantity:
            request.website.sale_reset()
            return value

        order = request.website.sale_get_order()
        value['cart_quantity'] = order.cart_quantity

        if not display:
            return value

        value['website_sale.cart_lines'] = request.env['ir.ui.view']._render_template("website_sale.cart_lines", {
            'website_sale_order': order,
            'date': fields.Date.today(),
            'suggested_products': order._cart_accessories(),
            'bom_products': line
        })
        value['website_sale.short_cart_summary'] = request.env['ir.ui.view']._render_template(
            "website_sale.short_cart_summary", {
                'website_sale_order': order,
               
            })
        return value
