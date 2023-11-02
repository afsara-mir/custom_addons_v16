import datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class RealEstate(models.Model):
    _name = 'real_estate.properties'
    _order = 'sequence, id desc'

    name = fields.Char(string="Title", required=True)
    sequence = fields.Integer(string='Sequence', help="Used to order stages")
    property_type = fields.Selection([('house', 'House'), ('apartment', 'Apartment')], string="Property Type")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available Date")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area")
    total_area = fields.Integer(string="Total Area", compute="_compute_total_area", store=True)
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Has Garage?")
    garden = fields.Boolean(string="Has Garden?")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    status = fields.Selection([('new', 'New'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], default='new',
                              readonly=True)
    property_type_id = fields.Many2one('real_estate.property_type', string="Property Type")
    property_tag_ids = fields.Many2many('real_estate.property_tag', string="Tags")
    property_offer_ids = fields.One2many("real_estate.property_offer", "models_id", string="Offers")
    property_type_inline_ids = fields.Many2one('real_estate.property_type',string='Properties')
    partner_id = fields.Many2one(related="property_offer_ids.partner_id")

    @api.depends('bedrooms', 'living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.bedrooms * record.living_area) + record.garden_area

    @api.constrains('garden', 'garden_area')
    def _check_garden_area(self):
        for record in self:
            if record.garden == True and record.garden_area == 0:
                raise ValidationError("Garden Area should be given")

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_orientation = 'north'
                record.garden_area = 10
            else:
                record.garden_orientation = False
                record.garden_area = False

    def action_set_status_sold(self):
        for record in self:
            if record.status == 'cancelled':
                raise UserError("Cannot sold a cancelled property")
            else:
                record.status = 'sold'

    def action_set_status_cancel(self):
        for record in self:
            if record.status == 'sold':
                raise UserError('Cannot cancel a sold property')
            else:
                record.status = 'cancelled'

    @api.constrains('expected_price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price < 0:
                raise ValidationError("The expected price must be greater than 0")

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0:
                raise ValidationError("The selling price must be greater than 0")

    @api.constrains('date_availability')
    def _check_date_availability(self):
        for record in self:
            if record.date_availability and record.date_availability < datetime.date.today():
                raise ValidationError("Past Date cannot be selected")

    @api.constrains('expected_price', 'selling_price')
    def _check_expected_offer_price(self):
        for rec in self:
            if rec.selling_price < ((rec.expected_price * 90)/100):
                raise UserError("Selling price cannot be less than 90% of the expected price")

    @api.ondelete(at_uninstall=False)
    def _check_deletion(self):
        for rec in self:
            if rec.status not in ('new', 'canceled'):
                raise UserError("You can only delete a sold property")

    def action_set_sale_order(self):
            sale_order = self.env['project.project'].create(
                {
                    'name': self.name
                }
            )



