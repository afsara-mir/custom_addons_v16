from odoo import api, fields, models, Command


class EstateAccount(models.Model):
    _inherit="estate.property"

    def action_to_sell(self):
        move_obj = self.env['account.move']
        partner_id = self.salesperson.id
        move_type = 'out_invoice'
        # journal_id = self.env['account.journal'].search([('code','=','Short_code')], limit = 1)

        values = {'partner_id': partner_id,
                  'move_type': move_type,
                  'narration': self.description,
                  # 'journal_id': journal_id.id,
                  }
        new_invoice = move_obj.create(values)

        #create invoice line
        invoice_lines = [
            Command.create({
                'name': 'Property Sale',
                'quantity': 1,
                'price_unit': (self.selling_price * 0.06) + 100.00,
            }),
            Command.create({
                'name': 'Admin Fees',
                'quantity': 1,
                'price_unit': 100.00,
            }),
        ]

        new_invoice.write({'invoice_line_ids': invoice_lines})

        print("The action_to_sell method is called")

        return super().action_to_sell()