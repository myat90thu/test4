# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DevliveryInherit(models.Model):
    _inherit = 'stock.picking'

    text = fields.Char(string='Test')
    place_mark = fields.Char(string='Place Mark')
    notes = fields.Char(string='Notes')