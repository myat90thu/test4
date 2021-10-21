# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class HrPayslip(models.Model):
	_inherit = 'hr.payslip'

	overtime_wages = fields.Float(compute="calc_overtime_wages",string='Overtime Hours Wages', store=True)

	@api.depends('employee_id')
	def calc_overtime_wages(self):
		for record in self:
			overtime_obj = self.env['hr.overtime.request']
			overtime_ids = overtime_obj.search([
				('employee_id','=', record.employee_id.id),
				('state','=', 'done'),
				('request_date','>=', record.date_from),
				('request_date','<=', record.date_to),
				])
			overtime_sum = sum((line.number_of_hours * line.hourly_wages) for line in overtime_ids)
			record.overtime_wages = overtime_sum