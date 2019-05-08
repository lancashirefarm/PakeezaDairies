# -*- coding: utf-8 -*-
from odoo import http

# class Cus(http.Controller):
#     @http.route('/cus/cus/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cus/cus/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cus.listing', {
#             'root': '/cus/cus',
#             'objects': http.request.env['cus.cus'].search([]),
#         })

#     @http.route('/cus/cus/objects/<model("cus.cus"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cus.object', {
#             'object': obj
#         })