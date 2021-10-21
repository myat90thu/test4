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


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    product_item_code = fields.Char(related="order_line.product_item_code", string='Product Item Code')

class Purchase(models.Model):
    _inherit = 'purchase.order.line'

    product_item_code = fields.Char(string='Product Item Code')
    product_brand = fields.Many2one('product.brand', string='Product Brand')
    part_number = fields.Char(string='Part Number')

    @api.onchange('product_id')
    def onchange_product_id(self):
        res = super(Purchase, self).onchange_product_id()
        self.product_item_code = self.product_id.product_item_code
        self.product_brand = self.product_id.product_brand
        self.part_number = self.product_id.part_number
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: