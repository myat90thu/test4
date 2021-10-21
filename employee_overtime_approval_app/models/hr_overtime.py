# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError, ValidationError


class HrOvertimeRequest(models.Model):
	_name = 'hr.overtime.request'
	_rec_name = 'employee_id'
	_description="Overtime Request"
	_inherit = ['mail.thread']


	def _default_employee(self):
		return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

	name = fields.Char(string='Name', readonly=True,
		states={'draft': [('readonly', False)]})
	state = fields.Selection([
		('draft', 'To Submit'),
		('validate1', 'Waiting For Department Manager'),
		('validate2', 'Waiting For Hr Manager'),
		('done', 'Done'),
		('refuse', 'Refused'),
	], string='Status', index=True, readonly=True, copy=False, default='draft')
	employee_id = fields.Many2one('hr.employee', string='Employee', index=True, readonly=True,
		states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]}, default=_default_employee, tracking=True)
	department_id = fields.Many2one('hr.department', string="Department", related="employee_id.department_id",readonly=True, tracking=True)
	dept_manager_id = fields.Many2one('hr.employee', string="Department Manager", readonly=True, states={'draft': [('readonly', False)]})
	dept_confirm_date = fields.Date('Confirm Date')
	request_date = fields.Date('Request Date', tracking=True, default=fields.Datetime.now)
	hr_confirm_date = fields.Date('Confirm Date')
	hr_manager_id = fields.Many2one('hr.employee', string="Hr Manager", readonly=True, states={'draft': [('readonly', False)]})
	job_id = fields.Many2one('hr.job', string='Job Position', related="employee_id.job_id",readonly=True, tracking=True)
	number_of_hours = fields.Float('Number of Hours', copy=False, readonly=True, states={'draft': [('readonly', False)]}, tracking=True)
	user_id = fields.Many2one('res.users', string='User', related='employee_id.user_id', related_sudo=True, compute_sudo=True, store=True, default=lambda self: self.env.uid, readonly=True)
	notes = fields.Text(string='Internal Note', readonly=True, states={'draft': [('readonly', False)]})
	rejected_by_id=fields.Many2one('res.users',string="Refused By",readonly=True)
	rejected_date = fields.Datetime(string="Refuse Date",readonly=True)
	rejected_reason=fields.Char(string="Refused Reason",readonly=True)
	hourly_wages = fields.Float('Hourly Wages')

	@api.model
	def create(self, vals):
		if vals.get('name', _('New')) == _('New'):
			if 'company_id' in vals:
				vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('hr.overtime.request') or _('New')
			else:
				vals['name'] = self.env['ir.sequence'].next_by_code('hr.overtime.request') or _('New')
		result = super(HrOvertimeRequest, self).create(vals)
		return result
		
	def action_confirm(self):
		for record in self:
			template_id = self.env['ir.model.data'].get_object_reference('employee_overtime_approval_app','overtime_request_email_template')[1]
			email_template_obj = self.env['mail.template'].browse(template_id)
			if template_id:
				values = email_template_obj.generate_email(self.id, ['subject', 'body_html', 'email_from', 'email_to', 'partner_to', 'email_cc', 'reply_to', 'scheduled_date','attachment_ids'])
				values['email_from'] = self.employee_id.user_id.partner_id.email or self.env.user.email or ''
				values['email_to'] = self.dept_manager_id.user_id.partner_id.email or ''
				values['author_id'] = self.env.user.partner_id.id
				values['subject'] = 'Overtime Request For ' + str(self.employee_id.name)
				body_html = "<p>Dear " + str(self.dept_manager_id.name or '') +",<p>" +\
							"<p>Overtime Request For "+ "<b>" + str(self.employee_id.name or '') + "</b>" + " required for your Approval.</p>" +\
							"<p><b>Here are the details,</b><p>" +\
							"<p>&nbsp;&nbsp;&nbsp;&nbsp;<b>Name           	  :</b> " + str(self.name or '') +"<p>" +\
							"<p>&nbsp;&nbsp;&nbsp;&nbsp;<b>Department 		  :</b> " + str(self.department_id.name or '') +"<p>" +\
							"<p>&nbsp;&nbsp;&nbsp;&nbsp;<b>Designation 		  :</b> " + str(self.job_id.name or '') +"<p>" +\
							"<p>&nbsp;&nbsp;&nbsp;&nbsp;<b>Overtime Hours     :</b> " + str(self.number_of_hours or '') +"<p>" +\
							"<p>&nbsp;&nbsp;&nbsp;&nbsp;<b>Reason For Overtime:</b> " + str(self.notes or '') +"<p>" +\
							"<p>Sincerely,</p>"+\
							"<p>" + str(self.employee_id.name) + "</p>"
				values['body_html'] = body_html 
				mail_mail_obj = self.env['mail.mail']
				msg_id = mail_mail_obj.sudo().create(values)
				if msg_id:
					msg_id.sudo().send()
			record.state = 'validate1'


	def action_department_approve(self):
		action = self.env.ref('employee_overtime_approval_app.action_department_accept_request_1').read()[0]
		return action


	def action_manager_confirm(self):
		action = self.env.ref('employee_overtime_approval_app.action_hr_manager_accept_request_1').read()[0]
		return action
		
	def action_refuse(self):
		action = self.env.ref('employee_overtime_approval_app.action_request_rejected').read()[0]
		return action

	def action_draft(self):
		for record in self:
			record.state = 'draft'

	def unlink(self):
		if any(self.filtered(lambda record: record.state not in ('draft', 'cancel'))):
			raise UserError(_('You cannot delete a overtime which is not draft or cancelled!'))
		return super(HrOvertimeRequest, self).unlink()

	@api.onchange('employee_id')
	def onchange_employee(self):
		for record in self:
			record.dept_manager_id = record.department_id.manager_id.id or False
			record.hr_manager_id = record.employee_id.parent_id.id or False