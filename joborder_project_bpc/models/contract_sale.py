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

from odoo import fields, models, api, _
from collections import defaultdict
from odoo.exceptions import UserError


class SaleContractedOrder(models.Model):
    _inherit = 'sale.contracted.order'

    project_id = fields.Many2one('project.project',string='Project',)
    job_order_number = fields.Char(string='Job Order Number')

class contractedOrderWizard(models.TransientModel):
    _inherit = 'sale.contracted.order.wizard'
    _description = 'Contracted order wizard'

    def create_sale_order(self):
        order_lines_by_customer = defaultdict(list)
        currency_id = 0
        pricelist_id = 0
        user_id = 0
        payment_term_id = 0
        active_id = False
        if self._context.get('active_model') == 'sale.contracted.order':
            active_id = self.env['sale.contracted.order'].browse(self._context.get('active_id'))
            # for line in active_id.line_ids.filtered(lambda l: l.original_uom_qty != 0.0):
            for line in self.line_ids.filtered(lambda l: l.qty != 0.0):
                if line.remaining_uom_qty < line.qty:
                    raise UserError(
                        _('You can\'t order more than the remaining quantities'))
                vals = {'product_id': line.product_id.id,
                        'name': line.product_id.name,
                        'product_uom': line.product_uom.id,
                        'sequence': line.contracted_line_id.sequence,
                        'price_unit': line.price_unit,
                        'job_cost_type':line.job_cost_type,
                        'contracted_order_line': line.contracted_line_id.id,
                        'product_uom_qty': line.qty,
                        'tax_id': [(6, 0, line.taxes_id.ids)]}
                order_lines_by_customer[active_id.partner_id.id].append((0, 0, vals))
                #active_id = self.env['sale.contracted.order'].browse(self._context.get('active_id'))
                if currency_id == 0:
                    currency_id = active_id.currency_id.id
                elif currency_id != active_id.currency_id.id:
                    currency_id = False

                if pricelist_id == 0:
                    pricelist_id = active_id.pricelist_id.id
                elif pricelist_id != active_id.pricelist_id.id:
                    pricelist_id = False

                if user_id == 0:
                    user_id = active_id.partner_id.id
                elif user_id != active_id.partner_id.id:
                    user_id = False

                if user_id == 0:
                    user_id = active_id.user_id.id
                elif user_id != active_id.user_id.id:
                    user_id = False

                if payment_term_id == 0:
                    payment_term_id = active_id.payment_term_id.id
                elif payment_term_id != active_id.payment_term_id.id:
                    payment_term_id = False
        elif self._context.get('active_model') == 'sale.contracted.order.line':
            active_id = self.env['sale.contracted.order.line'].browse(self._context.get('active_id'))

            for line in self.line_ids.filtered(lambda l: l.qty != 0.0):
                if line.remaining_uom_qty < line.qty:
                    raise UserError(
                        _('You can\'t order more than the remaining quantities'))
                vals = {'product_id': line.product_id.id,
                        'name': line.product_id.name,
                        'product_uom': line.product_uom.id,
                        'sequence': line.contracted_line_id.sequence,
                        'price_unit': line.price_unit,
                        'job_cost_type': line.job_cost_type,
                        'contracted_order_line': line.contracted_line_id.id,
                        'product_uom_qty': line.qty,
                        'tax_id': [(6, 0, line.taxes_id.ids)]}
                order_lines_by_customer[active_id.partner_id.id].append((0, 0, vals))
                if currency_id == 0:
                    currency_id = active_id.currency_id.id
                elif currency_id != active_id.currency_id.id:
                    currency_id = False

                if pricelist_id == 0:
                    pricelist_id = active_id.pricelist_id.id
                elif pricelist_id != active_id.pricelist_id.id:
                    pricelist_id = False

                if user_id == 0:
                    user_id = active_id.partner_id.id
                elif user_id != active_id.partner_id.id:
                    user_id = False

                if user_id == 0:
                    user_id = active_id.user_id.id
                elif user_id != active_id.user_id.id:
                    user_id = False

                if payment_term_id == 0:
                    payment_term_id = active_id.payment_term_id.id
                elif payment_term_id != active_id.payment_term_id.id:
                    payment_term_id = False

        if not order_lines_by_customer:
            raise UserError(_('An order can\'t be empty'))

        if not currency_id:
            raise UserError(_('Can not create Sale Order from Contracted '
                              'Order lines with different currencies'))

        res = []
        for customer in order_lines_by_customer:
            order_vals = {
                'partner_id': customer,
                'origin': self.contracted_order_id.name,
                'user_id': user_id,
                'currency_id': currency_id,
                'project_id': active_id.project_id.id,
                'job_order_number': active_id.job_order_number,
                'pricelist_id': pricelist_id,
                'payment_term_id': payment_term_id,
                'order_line': order_lines_by_customer[customer],
            }
            sale_order = self.env['sale.order'].create(order_vals)
            res.append(sale_order.id)
        return {
            'domain': [('id', 'in', res)],
            'name': _('Sales Orders'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'context': {'from_sale_order': True},
            'type': 'ir.actions.act_window'
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: