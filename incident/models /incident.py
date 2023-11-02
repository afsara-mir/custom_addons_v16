from odoo import api, fields, models
from datetime import datetime

class Incident(models.Model):
    _name = 'incident.record'
    _description = "Nature of the Incident"

    name = fields.Char(string='Person reporting the incident')
    date = fields.Datetime(default=lambda self: datetime.now(), string="Date of the incident")
    location = fields.Char(string='Site Location of Incident')

    event_type_product = fields.Selection([("product_stolen","Product Stolen"),
                                   ("product_lost", "Product Lost"),
                                   ("product_depreciated","Product Depreciated"),
                                   ("product_misplaced","Product misplaced"),
                                   ("product_damaged","Product Damaged")],
                                    string = "Type of event related to product")

    event_type_employee = fields.Selection([("employee_accident","Employee Accident"),
                                            ("employee_death","Employee Deceased")],
                                           string = "Event related to employee")






