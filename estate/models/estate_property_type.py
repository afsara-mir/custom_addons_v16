
from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type' #The name of the database, you will find this in the  models tab inside odoo
    _description = "Property data type"
    _order = "sequence, name, id"

    name = fields.Char(string = 'Type of Property', required = True)
    property_ids = fields.One2many('estate.property','property_type_id') #This is the inverse of a many to one field. The field relates one record of the co-model with multiple records of the current model
    sequence = fields.Integer('Sequence', default = 1, help = 'Used to order stages')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string = "Records")#there is only one field of property_type that will receive many offers

    def action_open_offers(self):
        self.ensure_one()
        return {
            'name': 'Related Offers',
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property.offer',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.offer_ids.ids)],
        }

    offer_count = fields.Integer(compute="_compute_offer", string="Offers", store=True)

    @api.depends("offer_ids")
    def _compute_offer(self):
        for record in self:
            matching_offers = record.offer_ids.filtered(lambda offer: offer.property_type_id == record)
            record.offer_count = len(matching_offers)



