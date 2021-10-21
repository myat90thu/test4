# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import datetime



class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    def _compute_is_manager(self):
        for sheet in self:
            sheet.is_manager = False
            if sheet.employee_id.parent_id.user_id.id == sheet.env.uid:
                sheet.is_manager = True

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('approved_manager', 'Approved By Manager'),
        ('approve', 'Approved'),
        ('post', 'Posted'),
        ('done', 'Paid'),
        ('cancel', 'Refused')
    ], string='Status', index=True, readonly=True, track_visibility='onchange', copy=False, default='draft',
        required=True, help='Expense Report State')
    is_manager = is_refused = fields.Boolean("Is manager", compute='_compute_is_manager')

    def action_manager_approve(self):
        for self_obj in self:
            self_obj.write({'state': 'approved_manager'})
        template_id = self.env['ir.model.data'].get_object_reference(
            'bi_employee_expense_double_approval',
            'email_template_hr_approved_expense_request1')[1]
        email_template_obj = self.env['mail.template'].sudo().browse(template_id)
        user = self.env['res.users'].browse(self._context.get('uid'))
        user_ids = []
        for user in self.env['res.users'].search([]):
            if self.env.ref('hr_expense.group_hr_expense_user') in user.groups_id:
                user_ids.append(user.partner_id.id)
        users = set(user_ids)
        user_ids = list(users)
        if template_id:
            values = email_template_obj.generate_email(self.id,fields=['subject', 'body_html', 'email_from', 'email_to', 'partner_to', 'email_cc', 'reply_to', 'scheduled_date'])
            values['email_from'] = self.env.user.partner_id.email
            partner_ids = self.env['res.partner'].browse(user_ids)
            emails = set(r.email for r in partner_ids)
            if emails:
                values['email_to'] = ','.join(str(emails))
            values['res_id'] = False
            values['author_id'] = user.partner_id.id
            values['notification'] = True
            mail_mail_obj = self.env['mail.mail']
            msg_id = mail_mail_obj.sudo().create(values)
            if msg_id:
                msg_id.sudo().send([msg_id])
        return

    def action_submit_sheet(self):
        res = super(HrExpenseSheet, self).action_submit_sheet()
        user = self.env.user
        c = user
        template_id = self.env['ir.model.data'].get_object_reference(
            'bi_employee_expense_double_approval',
            'email_template_manager_approved_expense_request')[1]
        email_template_obj = self.env['mail.template'].sudo().browse(template_id)
        user = self.env['res.users'].browse(self._context.get('uid'))
        if template_id:
            values = email_template_obj.generate_email(self.id,fields=['subject', 'body_html', 'email_from', 'email_to', 'partner_to', 'email_cc', 'reply_to', 'scheduled_date'])
            values['email_from'] = self.env.user.partner_id.email
            values['email_to'] = self.employee_id.parent_id.work_email
            values['res_id'] = False
            values['author_id'] = user.partner_id.id
            values['notification'] = True
            mail_mail_obj = self.env['mail.mail']
            msg_id = mail_mail_obj.sudo().create(values)
            if msg_id:
                msg_id.sudo().send([msg_id])
        return res


