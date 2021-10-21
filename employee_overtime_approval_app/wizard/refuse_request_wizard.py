from odoo import models, fields, api ,_
from datetime import datetime

class RequestRejectWizard(models.TransientModel):
	_name='request.reject.wizard'
	_description ='Reject Request'

	reason = fields.Char(string="Refuse Reason")

	def reject_button(self):
		current_id = self.env['hr.overtime.request'].browse(self.env.context.get('active_ids'))
		if current_id:
			if current_id.state == 'validate1':
				template_id = self.env['ir.model.data'].\
					get_object_reference('employee_overtime_approval_app','overtime_request_reject_department_email_template')[1]
				email_template_obj = self.env['mail.template'].browse(template_id)
				if template_id:
					values = email_template_obj.generate_email(current_id.id, ['subject', 'body_html', 'email_from', 'email_to', 'partner_to', 'email_cc', 'reply_to', 'scheduled_date','attachment_ids'])
					values['email_from'] = current_id.dept_manager_id.user_id.partner_id.email or self.env.user.email or '' 
					values['email_to'] = current_id.employee_id.user_id.partner_id.email or ''
					values['author_id'] = self.env.user.partner_id.id
					values['subject'] = 'Overtime Request Rejected For' + str(current_id.employee_id.name)
					body_html = "<p>Dear " + str(current_id.employee_id.name or '') +",<p>" +\
								"<p>Your Overtime Request " + str(current_id.name)+" Rejected.</p>" +\
								"<p>Regards,</p>"+\
								"<p>" + str(current_id.dept_manager_id.name) + "</p>"
					values['body_html'] = body_html 
					mail_mail_obj = self.env['mail.mail']
					msg_id = mail_mail_obj.sudo().create(values)
					if msg_id:
						msg_id.sudo().send()
			if current_id.state == 'validate2':
				template_id = self.env['ir.model.data'].\
					get_object_reference('employee_overtime_approval_app','overtime_request_reject_manager_email_template')[1]
				email_template_obj = self.env['mail.template'].browse(template_id)
				if template_id:
					values = email_template_obj.generate_email(current_id.id, ['subject', 'body_html', 'email_from', 'email_to', 'partner_to', 'email_cc', 'reply_to', 'scheduled_date','attachment_ids'])
					values['email_from'] = current_id.hr_manager_id.user_id.partner_id.email or self.env.user.email or '' 
					values['email_to'] = current_id.employee_id.user_id.partner_id.email or ''
					values['author_id'] = self.env.user.partner_id.id
					values['subject'] = 'Overtime Request Rejected For' + str(current_id.employee_id.name)
					body_html = "<p>Dear " + str(current_id.employee_id.name or '') +",<p>" +\
								"<p>Your Overtime Request " + str(current_id.name)+" Rejected.</p>" +\
								"<p>Regards,</p>"+\
								"<p>" + str(current_id.hr_manager_id.name) + "</p>"
					values['body_html'] = body_html 
					mail_mail_obj = self.env['mail.mail']
					msg_id = mail_mail_obj.sudo().create(values)
					if msg_id:
						msg_id.sudo().send()
			current_id.rejected_reason = self.reason
			current_id.rejected_by_id = self.env.user
			current_id.rejected_date = datetime.today()
			current_id.state = 'refuse'
			

