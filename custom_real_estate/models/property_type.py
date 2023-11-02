from odoo import models, fields, api


class PropertyType(models.Model):
    _name = "real_estate.property_type"

    name = fields.Char(string="Property Type", required=True)
    models_inline_id = fields.One2many("real_estate.properties", "property_type_inline_ids", string="Properties")
    offer_ids = fields.One2many('real_estate.property_offer', 'property_type_id', string="Offers")

    def action_open_offers(self):
        self.ensure_one()
        return {
            'name': 'Related Offers',
            'type': 'ir.actions.act_window',
            'res_model': 'real_estate.property_offer',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.offer_ids.ids)],
        }
