# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
{
    'name': 'Invoice Report',
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'category': 'sales',
    'website': 'http://www.acespritech.com',
    'version': '14.0.1.0.0',
    'summary': '''
                Account
            ''',
    'description': '''
                    This module used for invoice report.
                ''',
    'depends': ['base','account','account_reports'],
    'data': [
        'views/company_view.xml',
        'report/invoice_report_inherited.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
