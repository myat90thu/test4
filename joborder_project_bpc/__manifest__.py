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
    'name': 'Joborder and Project',
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'category': 'sales',
    'website': 'http://www.acespritech.com',
    'version': '14.0.1.0.0',
    'summary': '''
                This module used to add job order number and project name into Quotation,Contracted Order,Sales Order,Delivery,Invoice.
            ''',
    'description': '''
                    This module used to add job order number and project name into Quotation,Contracted Order,Sales Order,Delivery,Invoice.
                ''',
    'depends': ['base','sale_management','account', 'stock','sale_contracted_order','job_costing_management'],
    'data': [
        'views/joborder_project_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
