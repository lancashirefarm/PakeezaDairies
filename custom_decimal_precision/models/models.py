# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class CustomPosOrder(models.Model):
    _inherit = 'pos.order'


class CustomPosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    cus_price_unit = fields.Float(string='Unit Price', digits=dp.get_precision('Product Price'))
    price_unit = cus_price_unit