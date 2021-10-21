# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import models, fields, api


class Sale(models.Model):
    _inherit = 'sale.order'

    product_item_code = fields.Char(related="order_line.product_item_code", string='Product Item Code')

class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    product_item_code = fields.Char(string='Product Item Code')
    product_brand = fields.Many2one('product.brand', string='Product Brand')
    part_number = fields.Char(string='Part Number')

    @api.onchange('product_id', 'price_unit', 'product_uom', 'product_uom_qty', 'tax_id')
    def _onchange_discount(self):
        res = super(SaleOrder, self)._onchange_discount()
        self.product_item_code = self.product_id.product_item_code
        self.product_brand = self.product_id.product_brand
        self.part_number = self.product_id.part_number
        return res

    @api.onchange('product_item_code')
    def _onchange_product_item_code(self):
        if self.product_item_code:
            pro_id = self.env['product.product'].search([('product_item_code','=',self.product_item_code)], limit=1)
            self.write({'product_id':pro_id})


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: