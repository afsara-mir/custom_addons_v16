# from datetime import timedelta, date
# from odoo import api, models, fields
#
#
# class PropertyTask(models.Model):
#     _name = "real_estate.property_task"
#
#     pay_cycle = fields.Selection([('12', '12'), ('24', '24'), ('26', '26'), ('52', '52')], string="Pay Cycle")
#     # start_date = fields.Date(string="Start Date")
#     # end_date = fields.Date(string="End Date")
#     date_range_id = fields.One2many('date.range', 'property_task_id', string="Date Range")
#
#     @api.onchange('pay_cycle')
#     def _onchange_pay_cycle(self):
#         date_list = []
#         if self.pay_cycle == '12':
#             for x in range(1, 12):
#                 if self.start_date:
#                     self.end_date = self.start_date + timedelta(days=30)
#                 else:
#                     self.start_date = date.today()
#                     self.end_date = date.today() + timedelta(days=30)
#             date_list.append((self.start_date, self.end_date))
#
#         elif self.pay_cycle == '24':
#             for x in range(1, 24):
#                 if self.start_date:
#                     self.end_date = self.start_date + timedelta(days=15)
#                 else:
#                     self.start_date = date.today()
#                     self.end_date = date.today() + timedelta(days=15)
#             date_list.append((self.start_date, self.end_date))
#
#         elif self.pay_cycle == '26':
#             for x in range(1, 26):
#                 if self.start_date:
#                     self.end_date = self.start_date + timedelta(days=14)
#                 else:
#                     self.start_date = date.today()
#                     self.end_date = date.today() + timedelta(days=14)
#             date_list.append((self.start_date, self.end_date))
#
#         elif self.pay_cycle == '52':
#             for x in range(1, 52):
#                 if self.start_date:
#                     self.end_date = self.start_date + timedelta(days=7)
#                 else:
#                     self.start_date = date.today()
#                     self.end_date = date.today() + timedelta(days=7)
#             date_list.append((self.start_date, self.end_date))
#
#
# class DateRange(models.Model):
#     _name = "date.range"
#
#     pay_cycle = fields.Selection([('12', '12'), ('24', '24'), ('26', '26'), ('52', '52')], string="Pay Cycle")
#     start_date = fields.Date(string='Start Date')
#     end_date = fields.Date(string='End Date')
#     property_task_id = fields.Many2one('real_estate.property_task', string='Task')
#
#
