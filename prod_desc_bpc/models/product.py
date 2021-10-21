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


class Product(models.Model):
    _inherit = 'product.product'

    product_item_code = fields.Char(string='Product Item Code')
    product_brand = fields.Many2one('product.brand', string='Product Brand')
    part_number = fields.Char(string='Part Number')
    product_code = fields.Char(string='Product Code')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: