from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TravelTourPackage(models.Model):
    _name = "travel.package"
    _description = "Tour Package"
    _rec_name = "reference"

    reference = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    customer_id = fields.Many2one('res.partner', string='Customer', required=True, readonly=False, index=True)
    quotation_date = fields.Datetime(string='Quotation Date', default=fields.Datetime.today)
    source_id = fields.Many2one('customer.location', string='Source Location', required=True)
    destination_id = fields.Many2one('customer.location', string='Destination Location', required=True)
    travel_start = fields.Datetime(string="Travel Start Date", copy=False)
    travel_end = fields.Datetime(string="Travel End Date")
    no_of_travellers = fields.Integer(string='No of Travellers', default=1)
    facilities = fields.Many2many('travel.facilities', string='Facilities')
    vehicle_list = fields.Many2one('travel.vehicle', string="Vehicle List", required=True)

    service_id = fields.Many2one('travel.service', string="Service Type")

    vehicle_type = fields.Selection([
        ('bus', 'Bus'),
        ('traveller', 'Traveller'),
        ('van', 'Van'),
        ('other', 'Other')
    ], required=True)
    vehicle_estimation_line_ids = fields.One2many('travel_estimation', 'travel_package_id', string="Service",
                                                  required=True)

    # service_id = fields.Many2one('travel.service', string="Service Type")

    total = fields.Float(string='Total', compute='compute_total')

    @api.depends('vehicle_estimation_line_ids')
    def compute_total(self):
        if self.vehicle_estimation_line_ids:
            self.total = False
            for rec in self.vehicle_estimation_line_ids:
                self.total += rec.price
        else:
            self.total = False

    @api.onchange('vehicle_list')
    def onchange_vehicle(self):
        for rec in self:
            lines = [(5, 0, 0)]
            for line in self.vehicle_list.vehicle_charges_line_ids:
                vals = {
                    'quantity': line.quantity,
                    'service_id': line.service_id,
                    'unit': line.unit,
                    'price': line.price

                }
                lines.append((0, 0, vals))
            rec.vehicle_estimation_line_ids = lines

    @api.onchange('vehicle_type', 'no_of_travellers', 'travel_start', 'travel_end')
    def onchange_type_vehicle(self):
        for rec in self:
            return {'domain': {'vehicle_list': [('vehicle_type', '=', rec.vehicle_type),
                                                ('no_of_seats', '>=', rec.no_of_travellers)]}}

    @api.constrains('vehicle_list', 'travel_start', 'travel_end')
    def _check_vehicle_list(self):
        for rec in self:
            check = rec.env['travel.package'].search([('vehicle_list', '=', rec.vehicle_list.id),
                                                      ('travel_start', '<=', rec.travel_end),
                                                      ('travel_end', '>=', rec.travel_start),
                                                      ('id', '!=', rec.id)])
            if check:
                raise ValidationError("The vehicle not available on the selected date")

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('travel.package') or _('New')
        res = super(TravelTourPackage, self).create(vals)
        return res

    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirmed')], default='draft', string='Status')

    def action_confirm(self):
        self.state = "confirm"
        for rec in self:
            lines = [(5, 0, 0)]
            for line in self.vehicle_estimation_line_ids:
                val = {
                    'quantity': line.quantity,
                    'service_id': line.service_id,
                    'unit': line.unit,
                    'price': line.price

                }
                lines.append((0, 0, val))

            booking_create = self.env['travel.customer'].create(
                {
                    'customer_id': self.customer_id.id,
                    'no_of_passengers': self.no_of_travellers,
                    'source_id': self.source_id.id,
                    'destination_id': self.destination_id.id,
                    'travel_start_date': self.travel_start,
                    'travel_end_date': self.travel_end,
                    'service_id': self.service_id.id,
                    'estimation_price_line_ids': [(0, 0, val)]

                }

            )
            booking_create.action_confirm_()

    def action_draft(self):
        self.state = "draft"


class TravelVehicleEstimation(models.Model):
    _name = 'travel_estimation'
    _description = "Vehicle Estimation"

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
    price = fields.Float(string='Sub Total', compute="_compute", )
    travel_package_id = fields.Many2one('travel.package', string="ref")

    @api.depends('quantity', 'unit')
    def _compute(self):
        for line in self:
            line.price = line.unit * line.quantity

    # totals = fields.Float('Total', compute='compute_total')
    #
    # @api.depends(price)
    # def compute_total(self):
    #     self.totals += self.price
