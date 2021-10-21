# -*- coding: utf-8 -*-

{
    'name' : 'Odoo Employee Overtime Request and Approval App',
    'author': "Edge Technologies",
    'version' : '14.0.1.0',
    'live_test_url':'https://youtu.be/rOdIkYDXPr8',
    "images":["static/description/main_screenshot.png"],
    'summary' : 'Employee Overtime Request Employee Overtime approval request for overtime HR Overtime Request HR Overtime approval request for overtime request for employee overtime request with approval request for overtime employee overtime with payroll',
    'description' : """
        Odoo Employee Overtime Request Approval App
    """,
    'depends' : ['hr','hr_payroll','hr_payroll_account'],
    "license" : "OPL-1",
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/overtime_data.xml',
        'data/mail_template.xml',
        'wizard/departmet_accept_request_view.xml',
        'wizard/hr_manager_accept_request_view.xml',
        'wizard/refuse_request_wizard_view.xml',
        'views/hr_overtime_view.xml',
        'views/hr_payroll_view.xml'
            ],
    'qweb' : [],
    'demo' : [],
    'installable' : True,
    'auto_install' : False,
    'price': 12,
    'currency': "EUR",
    'category' : 'Human Resources',
}
