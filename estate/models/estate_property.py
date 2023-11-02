from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'  # The name of the database, you will find this in the  models tab inside odoo
    _description = "Real estate data"
    _order = "id desc"

    name = fields.Char(default='Unknown', string="Property Name",required=True)
    age = fields.Integer(string='Age')
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode', required=True)
    date_availability = fields.Datetime(default=lambda self: datetime.now() + relativedelta(months=3),
                                        string='Availability from')
    expected_price = fields.Float(string='Expected_price', required=True)

    selling_price = fields.Float(compute='_compute_selling_price', string='Selling price', copy=False, default=0.0)

    invoice_id = fields.Many2one('estate_account.new_invoice', string='Invoice')

    @api.depends('offer_ids')
    def _compute_selling_price(self):
        for record in self:
            if any(offer.status == 'accepted' for offer in record.offer_ids):
                accepted_price = [offer.price for offer in record.offer_ids if offer.status == 'accepted']
                record.selling_price = max(accepted_price)
            else:
                record.selling_price = 0.0

    bedrooms = fields.Integer(default=2, string='No. of bedrooms')
    living_area = fields.Float(string='Living space area (sqm)')
    facades = fields.Integer(string='No. of facades')
    garage = fields.Boolean(string='Has a garage')
    garden = fields.Boolean(string='Has a garden')

    garden_area = fields.Float(string='Garden space (sqm)')

    @api.onchange('garden', 'garden_area')
    def onchange_garden_area(self):
        if self.garden and self.garden_area == 0:
            self.garden_area = 10
        else:
            if not self.garden:
                self.garden_area = 0

    garden_orientation = fields.Selection([('north', 'North'),
                                           ('south', 'South'),
                                           ('east', 'East'),
                                           ('west', 'West')],
                                          string='Garden orientation')

    @api.onchange('garden', 'garden_orientation')
    def onchange_garden_orientation(self):
        if self.garden and not self.garden_orientation:
            self.garden_orientation = 'north'
        else:
            if not self.garden:
                self.garden_orientation = None

    is_property_owner = fields.Boolean(string='Is property owner?')
    notes = fields.Text(string='Notes')
    active = fields.Boolean(default=True, string='Active')
    state = fields.Selection([('new', 'New'),
                              ('offerReceived', 'Offer Received'),
                              ('offerAccepted', 'Offer Accepted'),
                              ('sold', 'Sold'), ('cancelled', 'Cancelled')],
                             string='Status', required=True, copy=False, default='new')


    @api.ondelete(at_uninstall=False)
    def unlink(self):
        # Check the state of each property before allowing deletion
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise ValidationError("You cannot delete a property with state other than 'New' or 'Canceled'.")

        return super(EstateProperty, self).unlink()

    old_state = fields.Selection([('new', 'New'),
                                  ('offerReceived', 'Offer Received'),
                                  ('offerAccepted', 'Offer Accepted'),
                                  ('sold', 'Sold'), ('cancelled', 'Cancelled')],
                                 compute='_compute_old_state', string='Old Status', store=True, readonly=True)

    @api.depends('state')
    def _compute_old_state(self):
        for record in self:
            record.old_state = record.state

    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female'),
                               ('others', 'Others')],
                              string='Gender')

    # relates the current model's record with one among many records in the co-model(second-model),
    # by convention the syntax contains the co-model name and a field name
    property_type_id = fields.Many2one("estate.property.type", string="Property type",
                                       required=True)

    # any number of records on the current model will be related to any number of records in the co-model
    property_tag_ids = fields.Many2many("estate.property.tag", 'name',
                                        string="Tags")

    _sql_constraints = [
        ('property_unique_tags', 'unique(property_tag_ids)',
         'The property tag of the properties must be unique field, the tag already exists'),
    ]

    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    inline_id = fields.Many2one('estate.property.type')
    salesperson = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)


    # compute the total area
    total_area = fields.Float(compute="_compute_total", search='_search_total_area', string='Total area')

    @api.depends('garden_area', 'living_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('garden_area', 'living_area')
    def _search_total_area(self, operator, value):
        search_area = value
        return [('total_area', '>=', search_area)]

    best_offer = fields.Float(compute="_compute_offer", search='_search_best_offer', string='Best offer')

    @api.depends("offer_ids.price")
    def _compute_offer(self):
        for record in self:
            if record.offer_ids:
                best_offer = max(record.offer_ids.mapped('price'))
                record.best_offer = best_offer
            else:
                record.best_offer = 0.0

    def _search_best_offer(self, operator, value):
        search_offer = value
        return [('best_offer', '>=', search_offer)]

    # another possible solution
    # @api.depends('offer_ids.price')
    # def _compute_offer(self):
    #     for record in self:
    #         prices = [item.price for item in record.offer_ids]
    #         if prices:
    #             record.best_offer = max(prices)
    #         else:
    #             record.best_offer = 0
    #


    def _check_state(self):
        for record in self:
            if record.state == 'sold' and record.old_state == 'cancelled':
                raise UserError("A cancelled property cannot be set as sold.")
            if record.state == 'cancelled' and record.old_state == 'sold':
                raise UserError("A sold property cannot be cancelled.")

    def action_to_sell(self):
        self.ensure_one()
        if self.state != 'cancelled':
            self.write({'state': 'sold'})
        else:
            raise UserError("Cannot set state to Sold for a canceled property.")

    def action_to_cancel(self):
        self.ensure_one()
        if self.state != 'sold':
            self.write({'state': 'cancelled'})
        else:
            raise UserError("Sold property cannot be cancelled.")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 50000 AND price <= 100000000)',
         'The price value of a house has to be between 50,000 and 100,000,000.')
    ]
