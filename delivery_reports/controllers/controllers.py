# -*- coding: utf-8 -*-
# from odoo import http


# class DeliveryReports(http.Controller):
#     @http.route('/delivery_reports/delivery_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/delivery_reports/delivery_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('delivery_reports.listing', {
#             'root': '/delivery_reports/delivery_reports',
#             'objects': http.request.env['delivery_reports.delivery_reports'].search([]),
#         })

#     @http.route('/delivery_reports/delivery_reports/objects/<model("delivery_reports.delivery_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('delivery_reports.object', {
#             'object': obj
#         })
