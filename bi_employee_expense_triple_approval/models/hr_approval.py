
from odoo import api, fields, models, _
from odoo.exceptions import UserError
class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('approved_manager', 'Approved By Manager'),
        ('approved_hr', 'Approved By Finance'),
        ('approve', 'Approved'),
        ('post', 'Posted'),
        ('done', 'Paid'),
        ('cancel', 'Refused')
    ], string='Status', index=True, readonly=True, track_visibility='onchange', copy=False, default='draft',
        required=True, help='Expense Report State')

    def approve_expense_sheets_gm(self):
        self.write({'state': 'approve'})


    def approve_expense_sheets(self):
        if not self.user_has_groups('hr_expense.group_hr_expense_team_approver'):
            raise UserError(_("Only Managers and HR Officers can approve expenses"))
        elif not self.user_has_groups('hr_expense.group_hr_expense_manager'):
            current_managers = self.employee_id.expense_manager_id | self.employee_id.parent_id.user_id | self.employee_id.department_id.manager_id.user_id

            if self.employee_id.user_id == self.env.user:
                raise UserError(_("You cannot approve your own expenses"))

            if not self.env.user in current_managers and not self.user_has_groups('hr_expense.group_hr_expense_user') and self.employee_id.expense_manager_id != self.env.user:
                raise UserError(_("You can only approve your department expenses"))

        responsible_id = self.user_id.id or self.env.user.id
        self.write({'state': 'approve', 'user_id': responsible_id})
        self.activity_update()

    def approve_hr_expense_sheets(self):
        for self_obj in self:
            self_obj.write({'state': 'approved_hr'})
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
            values = email_template_obj.generate_email(self.id, fields=['subject', 'body_html', 'email_from', 'email_to', 'partner_to', 'email_cc', 'reply_to', 'scheduled_date'])
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

    # current_user = fields.Many2one('res.users', compute='_get_current_user')
    #
    # @api.depends()
    # def _get_current_user(self):
    #     for rec in self:
    #         rec.current_user = self.env.user

    def action_manager_approve(self):

        for self_obj in self:
            self_obj.write({'state': 'approved_manager'})
        template_id = self.env['ir.model.data'].get_object_reference(
            'bi_employee_expense_triple_approval',
            'email_template_hr_approved_expense_request12')[1]
        email_template_obj = self.env['mail.template'].sudo().browse(template_id)
        user = self.env['res.users'].browse(self._context.get('uid'))

        user_ids = []
        for user in self.env['res.users'].search([]):
            if self.env.ref('hr.group_hr_manager') in user.groups_id:
                user_ids.append(user.partner_id.id)
        users = set(user_ids)
        user_ids = list(users)

        if template_id:
            values = email_template_obj.generate_email(self.id, fields=['subject', 'body_html', 'email_from', 'email_to', 'partner_to', 'email_cc', 'reply_to', 'scheduled_date'])
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