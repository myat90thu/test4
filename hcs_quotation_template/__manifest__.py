# -*- coding: utf-8 -*-
{
    'name': "Quotation Template",

    'summary': """
        HCS Quotation Template""",

    'author': "HCS/Nadir",

    'depends': ['sale_management'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'data/email_template.xml',
    ],
}
