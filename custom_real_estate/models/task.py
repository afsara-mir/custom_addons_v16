# from odoo import models, fields, api
# from datetime import timedelta, date
#
# class Task(models.Model):
#     _name = 'real_estate.task'
#     start_date = fields.Date(string="Start Date")
#     end_date = fields.Date(string="End Date")
#     pay_cycle = fields.Selection([('12', '12'), ('24', '24'), ('26', '26'), ('52', '52')], string="Pay Cycle")
#     range_ids = fields.One2many('real_estate.range', 'task_id', string="Date Range")
#
#     @api.onchange('pay_cycle')
#     def _onchange_pay_cycle(self):
#         date_list = []
#         start_date = date.today()
#         current_date = start_date
#
#         if self.pay_cycle == '12':
#             for x in range(1, 12):
#                 end_date = current_date + timedelta(days=30)
#                 date_list.append((current_date, end_date))
#                 current_date = end_date + timedelta(days=1)
#
#         if self.pay_cycle == '24':
#             for x in range(1, 24):
#                 end_date = current_date + timedelta(days=15)
#                 date_list.append((current_date, end_date))
#                 current_date = end_date + timedelta(days=1)
#
#         if self.pay_cycle == '26':
#             for x in range(1, 26):
#                 end_date = current_date + timedelta(days=14)
#                 date_list.append((current_date, end_date))
#                 current_date = end_date + timedelta(days=1)
#
#         if self.pay_cycle == '52':
#             for x in range(1, 52):
#                 end_date = current_date + timedelta(days=7)
#                 date_list.append((current_date, end_date))
#                 current_date = end_date + timedelta(days=1)
#
#         return date_list
#
#     data={
#         "name": "Test",
#         "start_date":"",
#         "end_date":"",
#     }
#
# class Range(models.Model):
#     _name = 'real_estate.range'
#
#
#     name= fields.Char("Name")
#     start_date = fields.Date(string="Start Date")
#     end_date = fields.Date(string="End Date")
#     task_id = fields.Many2one('real_estate.task', string='Task')