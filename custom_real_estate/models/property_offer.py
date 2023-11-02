from datetime import timedelta
from odoo.exceptions import ValidationError, UserError
from odoo import fields, api, models


class PropertyOffer(models.Model):
    _name = "real_estate.property_offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], readonly=True)
    partner_id = fields.Many2one("res.partner", required=True)
    models_id = fields.Many2one("real_estate.properties", required=True)
    offer_date = fields.Date(string="Offer Date")
    validity = fields.Integer(string="Offer Validity(days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_deadline', store=True)
    property_type_id = fields.Many2one(related='models_id.property_type_id')

    @api.depends('offer_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            if record.offer_date and record.validity:
                offer_date = fields.Date.from_string(record.offer_date)
                date_deadline = offer_date + timedelta(days=record.validity)
                record.date_deadline = fields.Date.to_string(date_deadline)
            else:
                record.date_deadline = False

    # @api.constrains('offer_date')
    # def _check_offer_date(self):
    #     for record in self:
    #         if record.offer_date and record.offer_date < fields.Date.today():
    #             raise ValidationError("Past Date cannot be selected")

    def action_accepted(self):
        for rec in self:
            if rec.status == 'refused':
                raise UserError("Cannot accept an refused offer")
            else:
                rec.status = 'accepted'

    def action_refused(self):
        for rec in self:
            if rec.status == 'accepted':
                raise UserError("Cannot reject an accepted offer")
            else:
                rec.status = 'refused'
