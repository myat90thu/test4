# -*- coding: utf-8 -*-
{
    'name': "Inherit CRM",
    'summary': """
        This module hide and change some fields and button attributes
    """,
    'author': "Muhammad Imran",
    'depends': ['base', 'crm', 'sale_crm', 'sale_contracted_order', 'job_costing_management', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'data/lead_sequence.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
}
