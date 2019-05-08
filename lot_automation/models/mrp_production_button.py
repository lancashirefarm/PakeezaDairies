from odoo import models, api


class Custom(models.Model):
    _inherit = 'mrp.production'


    @api.multi
    def custom_open_produce_product(self):
        self.ensure_one()
        action = self.env.ref('lot_automation.custom_act_mrp_product_produce').read()[0]
        print(action)
        return action