from odoo import models, fields, api


class TravelVehicle(models.Model):
    _name = "travel.vehicle"
    _description = "Travel vehicle"
    _rec_name = "vehicle_name"

    registration_no = fields.Char('Registration No', required=True)
    vehicle_type = fields.Selection([
        ('bus', 'Bus'),
        ('traveller', 'Traveller'),
        ('van', 'Van'),
        ('other', 'Other')
    ], required=True)

    vehicle_name = fields.Char('Name', compute='_compute_vehicle_name', default=' ')
    no_of_seats = fields.Integer(string='No of Seats', default=1)
    facilities = fields.Many2many('travel.facilities', string='Facilities')
    vehicle_charges_line_ids = fields.One2many('travel.charges', 'travel_vehicle_id', string="Service")

    _sql_constraints = [
        (
            'name_registration_no_unique', 'unique (registration_no)',
            "A Registration No already exists with this name . Registration No name must be unique!"),
    ]

    @api.depends('registration_no', 'vehicle_type')
    def _compute_vehicle_name(self):
        # self.vehicle_name =str(self.registration_no or ""),""
        for rec in self:
            rec.vehicle_name = str(rec.registration_no or "") + "-" + str(rec.vehicle_type or "")


class TravelFacilities(models.Model):
    _name = "travel.facilities"
    _description = "Travel facilities"
    _rec_name = 'facilities'
    facilities = fields.Char('Facilities')


class TravelVehicleCharges(models.Model):
    _name = 'travel.charges'
    _description = "Vehicle charges"

    service_id = fields.Selection([
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('bus', 'Bus'),
    ])
    quantity = fields.Integer(string="Quantity", default="1")
    unit = fields.Integer(string='Unit Price')
    price = fields.Integer(string='Sub Total', compute="_compute_price_")
    travel_vehicle_id = fields.Many2one('travel.vehicle', string="ref")

    @api.depends('quantity', 'unit')
    def _compute_price_(self):
        for line in self:
            line.price = line.unit * line.quantity
