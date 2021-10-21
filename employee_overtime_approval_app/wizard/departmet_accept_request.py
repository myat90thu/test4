# -*- coding: utf-8 -*-

from odoo import models, fields, api ,_
from datetime import datetime
from odoo.exceptions import UserError, ValidationError

class DepartmentAcceptRequest(models.TransientModel):
	_name='department.accept.request'
	_description ='Department Accept Request'

	
	confirm_date = fields.Date('Confirm Date', required=True)

	def confirm_button(self):
		current_id = self.env['hr.overtime.request'].browse(self.env.context.get('active_ids'))
		if current_id:
			template_id = self.env['ir.model.data'].\
				get_object_reference('employee_overtime_approval_app','overtime_request_approve_department_email_template')[1]
			email_template_obj = self.env['mail.template'].browse(template_id)
			if template_id:
				values = email_template_obj.generate_email(current_id.id, ['subject', 'body_html', 'email_from', 'email_to', 'partner_to', 'email_cc', 'reply_to', 'scheduled_date','attachment_ids'])
				values['email_from'] = current_id.dept_manager_id.user_id.partner_id.email or self.env.user.email or '' 
				values['email_to'] = current_id.hr_manager_id.user_id.partner_id.email or self.env.user.email or '' 
				values['author_id'] = self.env.user.partner_id.id
				values['subject'] = 'Overtime Request For ' + str(current_id.employee_id.name) + ' Confirmation'
				body_html = "<p>Dear " + str(current_id.hr_manager_id.name or '') +",<p>" +\
							"<p>Overtime Request For "+ "<b>" + str(current_id.employee_id.name or '') + "</b>" + " required for your confirmation.</p>" +\
							"<p><b>Here are the details,</b><p>" +\
							"<p>&nbsp;&nbsp;&nbsp;&nbsp;<b>name           	  :</b> " + str(current_id.name or '') +"<p>" +\
							"<p>&nbsp;&nbsp;&nbsp;&nbsp;<b>Department 		  :</b> " + str(current_id.department_id.name or '') +"<p>" +\
							"<p>&nbsp;&nbsp;&nbsp;&nbsp;<b>Designation 		  :</b> " + str(current_id.job_id.name or '') +"<p>" +\
							"<p>&nbsp;&nbsp;&nbsp;&nbsp;<b>Overtime Hours     :</b> " + str(current_id.number_of_hours or '') +"<p>" +\
							"<p>&nbsp;&nbsp;&nbsp;&nbsp;<b>Reason For Overtime:</b> " + str(current_id.notes or '') +"<p>" +\
							"<p>Regards,</p>"+\
							"<p>" + str(current_id.dept_manager_id.name) + "</p>"
				values['body_html'] = body_html 
				mail_mail_obj = self.env['mail.mail']
				msg_id = mail_mail_obj.sudo().create(values)
				if msg_id:
					msg_id.sudo().send()
			current_id.dept_confirm_date = self.confirm_date
			current_id.state = 'validate2'


	@api.onchange('confirm_date')
	def _check_confirm_date(self):
		current_id = self.env['hr.overtime.request'].browse(self.env.context.get('active_ids'))
		if self.confirm_date:
			if self.confirm_date < current_id.request_date:
				raise ValidationError(_("Overtime 'Confirm Date' must be before 'Request Date'."))
			

