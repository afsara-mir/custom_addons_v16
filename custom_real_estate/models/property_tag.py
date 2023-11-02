from odoo import models, fields, api


class PropertyTag(models.Model):
    _name = "real_estate.property_tag"

    name = fields.Char(string="Property Tag", required=True)
    color = fields.Integer(string="Color")
