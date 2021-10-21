# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AnalyticAccount(models.Model):
    _inherit = 'hr.employee'

    analytic_account = fields.Many2many('account.analytic.account', string='Analytic Account')


class HrExpenseInherit(models.Model):
    _inherit = 'hr.expense'

    @api.onchange('employee_id')
    def _onchange_partner_ids(self):
        id = self.employee_id.id
        analytic_employee = self.env['hr.employee'].browse(id)
        c = []
        for m in analytic_employee.analytic_account:
            c.append(m.id)
        if c:
           return {'domain': {'analytic_account_id': [('id', 'in', c)]}}
        return {'domain': {'analytic_account_id': [('id', 'not in', c)]}}




