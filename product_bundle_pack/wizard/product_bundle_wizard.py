# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime, timedelta, date

class bi_wizard_product_bundle(models.TransientModel):
    _name = 'wizard.product.bundle.bi'
    _description = "Wizard Product Bundle"

    product_id = fields.Many2one('product.product', string='Group', required=True)
    total_discount = fields.Float(related='product_id.total_discount', string='Total Discount', readonly=True)
    total_ulp = fields.Float(related='product_id.total_ulp', string='Total Unit List Price', readonly=True)
    total_unp = fields.Float(related='product_id.total_unp', string='Total Unit Net Price', readonly=True)
    total_tnp = fields.Float(related='product_id.total_tnp', string='Total Net Price', readonly=True)
    total_ulc = fields.Float(related='product_id.total_ulc', string='Total Unit landed Cost', readonly=True)
    total_tlc = fields.Float(related='product_id.total_tlc', string='Total landed Cost', readonly=True)
    total_ucoh = fields.Float(related='product_id.total_ucoh', string='Total U.Cost/OH', readonly=True)
    total_tcoh = fields.Float(related='product_id.total_tcoh', string='Total Cost/OH', readonly=True)
    total_usp = fields.Float(related='product_id.total_usp', string='Total Unit Selling Price', )
    total_tsp = fields.Float(related='product_id.total_tsp', string='Total Selling Price', readonly=True)

    pack_ids = fields.One2many('product.group.line', related='product_id.group_lines', string="Select Products")

    def button_add_product_bundle_bi(self):
        job_order = self.env['job.costing'].browse(self._context.get('active_id'))
        for pack in self:
            if pack.product_id.is_pack:
                test = self.env['job.cost.line'].\
                    create({'direct_id':self._context['active_id'],
                            'product_id':pack.product_id.id,
                            'job_type': 'material',
                            'name':pack.product_id.name,
                            'product_qty': 1,
                            'discount': self.total_discount,
                            'unit_list_price': self.total_ulp,
                            'unit_net_price': self.total_unp,
                            'total_net_price': self.total_tnp,
                            'unit_landed_cost': self.total_ulc,
                            'total_landed_cost': self.total_tlc,
                            'unit_cost_oh': self.total_ucoh,
                            'total_cost_oh': self.total_tcoh,
                            'unit_selling_price': self.total_usp,
                            'total_selling_price': self.total_tsp,
                            })
        return True

