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


class Account(models.Model):
    _inherit = 'account.move'

    product_item_code = fields.Char(related="invoice_line_ids.product_item_code", string='Product Item Code')

class AccountMove(models.Model):
    _inherit = 'account.move.line'

    product_item_code = fields.Char(string='Product Item Code')
    product_brand = fields.Many2one('product.brand', string='Product Brand')
    part_number = fields.Char(string='Part Number')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super(AccountMove, self)._onchange_product_id()
        self.product_item_code = self.product_id.product_item_code
        self.product_brand = self.product_id.product_brand
        self.part_number = self.product_id.part_number
        return res

    def create(self, vals):
        if isinstance(vals, list):
            for rec in vals:
                product_id = self.env['product.product'].browse(rec.get('product_id'))
                rec.update({'product_item_code': product_id.product_item_code,
                            'product_brand': product_id.product_brand.id,
                            'part_number': product_id.part_number})
        res = super(AccountMove, self).create(vals)
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: