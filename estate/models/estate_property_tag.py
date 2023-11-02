from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag' #The name of the database, you will find this in the  models tab inside odoo
    _description = "Property tag information"
    _order = "name"

    name = fields.Char(string = 'Tag name')
    color_tags = fields.Integer(string = "Color")



