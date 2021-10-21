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

from odoo import models, fields, api,_


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one(
        'project.project', related='job_cost_id.project_id',
        string='Project',
        store=True
    )
    job_order_number = fields.Char(
        related='job_cost_id.job_order_number', 
        string='Job Order Number',
        store=True
    )

    def create_blanket_order(self):
        line_list = []
        res = []
        for line in self.order_line:
            if line.product_id:
                line_dict = {'product_id': line.product_id.id,
                             'name': line.name,
                             'original_uom_qty': line.product_uom_qty,
                             'product_uom': line.product_uom.id,
                             'price_unit': line.price_unit,
                             'taxes_id': line.tax_id.id,
                             'price_subtotal': line.price_subtotal,
                             'job_cost_type': line.job_cost_type
                             }
                line_list.append((0, 0, line_dict))

        vals = {'partner_id': self.partner_id.id,
                'pricelist_id': self.pricelist_id.id,
                'payment_term_id': self.payment_term_id.id,
                'validity_date': self.validity_date,
                'project_id': self.project_id.id,
                'job_order_number': self.job_order_number,
                'user_id': self.user_id.id,
                'team_id': self.team_id.id,
                'company_id': self.company_id.id,
                'fiscal_position_id': self.fiscal_position_id.id,
                'amount_untaxed': self.amount_untaxed,
                'amount_tax': self.amount_tax,
                'amount_total': self.amount_total,
                'line_ids': line_list
                }
        contracted_order = self.env['sale.contracted.order'].create(vals)

        res.append(contracted_order.id)
        self.state = "contracted"
        return {
            'domain': [('id', 'in', res)],
            'name': _('Contracted Orders'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.contracted.order',
            # 'context': {'from_sale_order': True},
            'type': 'ir.actions.act_window'
        }

    def action_confirm(self):
        res = super(SaleOrder,self).action_confirm()
        for order in self:
            warehouse = order.warehouse_id
            if order.picking_ids:
                for picking in self.picking_ids:
                    picking.write({'project_id': self.project_id.id,
                               'job_order_number': self.job_order_number})
                    picking.action_assign()
                    picking.action_confirm()
                    for mv in picking.move_ids_without_package:
                        mv.quantity_done = mv.product_uom_qty
        return res

    def _create_invoices(self, grouped=False, final=False, start_date=None, end_date=None):
        invoice = super(SaleOrder,self)._create_invoices(grouped, final)
        invoice.write({'project_id': self.project_id.id,
                   'job_order_number': self.job_order_number})
        return invoice
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
