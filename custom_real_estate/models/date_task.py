from odoo import api, fields, models
from datetime import timedelta, date, datetime


class DateTask(models.Model):
    _name = 'date.task'

    pay_cycle = fields.Selection([('12', '12'), ('24', '24'), ('26', '26'), ('52', '52')], string="Pay Cycle")
    date_lists = fields.One2many('date.list', 'date_task', string="Date Range")

    @api.onchange('pay_cycle')
    def _onchange_pay_cycle(self):
        date_list = []
        start_date = date.today().replace(day=1, month=1)
        current_date = start_date

        self.date_lists.unlink()

        if self.pay_cycle == '12':
            for x in range(1, 12):
                end_date = current_date + timedelta(days=30)
                date_list.append((0, 0, {
                    'start_date': current_date,
                    'end_date': end_date,
                }))
                current_date = end_date + timedelta(days=1)

        if self.pay_cycle == '24':
            for x in range(1, 24):
                end_date = current_date + timedelta(days=15)
                date_list.append((0, 0, {
                    'start_date': current_date,
                    'end_date': end_date,
                }))
                current_date = end_date + timedelta(days=1)

        if self.pay_cycle == '26':
            for x in range(1, 26):
                end_date = current_date + timedelta(days=14)
                date_list.append((0, 0, {
                    'start_date': current_date,
                    'end_date': end_date,
                }))
                current_date = end_date + timedelta(days=1)

        if self.pay_cycle == '52':
            for x in range(1, 52):
                end_date = current_date + timedelta(days=7)
                date_list.append((0, 0, {
                    'start_date': current_date,
                    'end_date': end_date,
                }))
                current_date = end_date + timedelta(days=1)

        self.date_lists = date_list


class DateList(models.Model):
    _name = 'date.list'

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    date_task = fields.Many2one('date.task', string="Task")
