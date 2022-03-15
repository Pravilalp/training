from datetime import timedelta

from odoo import fields, models, _, api
from odoo.exceptions import ValidationError


class TravelManagement(models.Model):
    _name = "travel.customer"
    _description = "Travel management"
    _rec_name = 'reference'

    reference = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))

    customer_id = fields.Many2one('res.partner', string='Customer', required=True, index=True,
                                  domain="[ ('is_company', '=', True)]"
                                  )

    no_of_passengers = fields.Integer(string='No of Passengers', default=1)
    service = fields.Selection([
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('bus', 'Bus'),
    ], default='bus')
    fees = fields.Integer(string="Fees", invisible=True)
    service_id = fields.Many2one('travel.service', string="Service Type")
    booking_date = fields.Datetime(string='Booking Date', default=fields.Datetime.today)
    source_id = fields.Many2one('customer.location', string='Source Location')
    destination_id = fields.Many2one('customer.location', string='Destination Location')
    travel_start_date = fields.Date(string="Travel Start Date")
    travel_end_date = fields.Date(string="Travel End Date")
    expiration_date = fields.Date(string="Expiration Date", compute='_compute_expiration_date', readonly=False)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirmed'),
                              ('expired', 'Expired'), ('create_invoice', 'Invoiced')], default='draft',
                             string='Status')

    estimation_price_line_ids = fields.One2many('estimation.price', 'travel_customer_id', string="Service")

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    totals = fields.Float(string='Total', compute="_compute_totals")

    @api.depends('estimation_price_line_ids')
    def _compute_totals(self):
        if self.estimation_price_line_ids:
            self.totals = False
            for rec in self.estimation_price_line_ids:
                self.totals += rec.price
        else:
            self.totals = False

    @api.constrains('travel_end_date')
    def _check_travel_end_date(self):
        for rec in self:
            if rec.travel_end_date < rec.travel_start_date:
                raise ValidationError('Travel end date cannot be less than the start date')

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('travel.customer') or _('New')
        res = super(TravelManagement, self).create(vals)
        return res

    @api.depends('service_id', 'booking_date')
    def _compute_expiration_date(self):
        for rec in self:
            rec.expiration_date = rec.booking_date + timedelta(days=rec.service_id.expiration_period)

    def action_confirm_(self):
        self.state = "confirm"

    def action_draft(self):
        self.state = "draft"

    def action_invoice(self):
        self.state = 'create_invoice'
        if self.service_id:
            lines = []
            for rec in self.estimation_price_line_ids:
                lines.append({'name': rec.service_id,
                              'price_unit': rec.price})
            print(lines)

            create_invoice = self.env['account.move'].create({
                'partner_id': self.customer_id.id,
                'move_type': 'out_invoice',
                'invoice_origin': self.reference,
                'invoice_line_ids': lines
            })
        else:

            create_invoice = self.env['account.move'].create({
                'partner_id': self.customer_id.id,
                'move_type': 'out_invoice',
                'invoice_origin': self.reference,
                'invoice_line_ids': [(0, 0, {'name': self.reference + "-" + self.service,
                                             'price_unit': self.fees})]
            })

        return {
            'name': _('create_invoice'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move',
            'view_id': self.env.ref('account.view_move_form').id,
            'target': 'current',
            'res_id': create_invoice.id,
        }

    def check_invoice(self):
        inv = self.env['account.move'].search([('invoice_origin', '=', self.reference)])
        print(inv)
        return {
            'name': 'create_invoiced',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move',
            'view_id': self.env.ref('account.view_move_form').id,
            'target': 'current',
            'res_id': inv.id,
        }

    @api.model
    def action_scheduler(self):
        customer_ids = self.env['travel.customer'].search([('expiration_date', '=', fields.date.today()),
                                                           ('state', '=', 'draft')])
        for rec in customer_ids:
            rec.state = 'expired'


class CustomerLocation(models.Model):
    _name = "customer.location"
    _description = "Customer Location"
    _rec_name = "city"

    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State',
                               index=True, domain="[ ('country_id', '=', country_id)]")

    country_id = fields.Many2one('res.country', string='Country')


class TravelEstimationPrice(models.Model):
    _name = 'estimation.price'
    _description = "Estimation Price"

    service_id = fields.Selection([
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('bus', 'Bus'),
    ])
    quantity = fields.Integer(string="Quantity", default="1")
    unit = fields.Integer(string='Unit Price')
    # price = fields.Integer(string='Sub Total', compute="_compute")
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id)
    price = fields.Float(string='Sub Total', compute="_compute")
    travel_customer_id = fields.Many2one('travel.customer', string="ref")

    @api.depends('quantity', 'unit')
    def _compute(self):
        for line in self:
            line.price = line.unit * line.quantity
