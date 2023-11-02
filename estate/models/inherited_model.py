from odoo import models, fields, api

class ResUsers(models.Model):
      # The name of the database, you will find this in the  models tab inside odoo

    _inherit = "res.users"

    property_ids = fields.One2many('estate.property',
                                   'salesperson',
                                   string='Properties',
                                   domain="[('state', 'in', ('new', 'offerReceived'))]"
                                   )

