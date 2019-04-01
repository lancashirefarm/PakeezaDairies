# -*- coding: utf-8 -*-
{
    'name': "Custom Header",

    'summary': """
        This module is develope to customise the headers color,button's color and highlight the manadotary fields 
	in odoo default theme. The process is done under maintance of oodles technologies.One of our developes 
	names as sahil dwivedi has done this Job.""",

    'description': """
        Change color of default odoo color theme 
    """,

    'author': "Sahil Dwivedi",
    'website': "https://www.oodlestechnologies.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Theme',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/header.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
