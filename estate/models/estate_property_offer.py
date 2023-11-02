from odoo import api, fields, models
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'  # The name of the database, you will find this in the  models tab inside odoo
    _description = "Offers made on the property"
    _rec_name = 'offer_partner_id'
    _order = "price desc"

    price = fields.Float(string='Price', required=True)
    status = fields.Selection([('accepted', 'Accepted'),
                               ('refused', 'Refused'),
                               ('pending', 'Pending')],
                              string='Status', copy=False)
    # A single property can be of interest to multiple buyers #the field receives from many
    property_id = fields.Many2one('estate.property', string = 'Property')
    @api.model
    def create(self, vals):
        existing_offer = self.search([('property_id', '=', vals.get('property_id')), ('price', '>', vals.get('price'))], limit=1)
        if existing_offer:
            raise ValidationError("The offer price cannot be lower than any of the existing offer")
        property_record= self.env['estate.property'].browse(vals.get('property_id'))
        if property_record:
            property_record.write({'state':'offerAccepted'})
        return super(EstatePropertyOffer, self).create(vals)

    # there are many offers for one property_type (eg:apartment)
    property_type_id = fields.Many2one(related="property_id.property_type_id")
    @api.constrains('price')
    def _check_offer(self):
        for record in self:
            if record.price < 0.9 * record.property_id.expected_price:
                raise ValidationError(
                    f"The offer price can only be 10% less than expected "
                    f"price {record.property_id.expected_price} which is {record.property_id.expected_price* 0.9}.")


    offer_partner_id = fields.Many2one('res.partner',string="Partner") #current model = property_offer and
    # co-model = res.partner : one record of the current model relates to many records of the co-model #one offer record but many propective buyers

    # def name_get(self):
    #     result = []
    #     for record in self:
    #         name = record.offer_partner_id.name # + ' - ' + record.property_id.name
    #         result.append((record.id, name))
    #     return result

    create_date = fields.Datetime(string = 'Creation date', default = lambda self: fields.Datetime.now())
    validity = fields.Integer(default = 7, string = 'Offer Validity(days)')
    date_deadline = fields.Datetime(compute = '_compute_total', inverse = '_inverse_total', string = 'Offer expires after')

    @api.depends("validity", "create_date")
    def _compute_total(self):
        for record in self:
            if record.validity and record.create_date:
                record.date_deadline = record.create_date + timedelta(days = record.validity)

    def _inverse_total(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - record.create_date).days

    def action_to_accept(self):
        self.ensure_one()
        if self.status != 'refused':
            self.write({'status': 'accepted'})
        else:
            raise UserError("Rejected offer cannot be accepted.")

    def action_to_reject(self):
        self.ensure_one()
        if self.status != 'accepted':
            self.write({'status': 'refused'})
        else:
            raise UserError("Accepted offer cannot be rejected.")

    _sql_constraints = [
        ('check_price', 'CHECK(price >= 50000 AND price <= 100000000)',
         'The price value of a house has to be between 50,000 and 100,000,000.')
    ]





