# -*- coding: utf-8 -*-

{
    'name': 'Custom POS Logo',
    'version': '12.0.1.0.0',
    'summary': """Logo For Every Point of Sale (Screen & Receipt)""",
    'description': """"This module helps you to set a logo for every point of sale. This will help you to
                 identify the point of sale easily. You can also see this logo in pos screen and pos receipt.""",
    'category': 'Point Of Sale',
    'author': 'Custom',
    'company': 'Test',
    'website': "https://www.google.com/",
    'depends': ['base', 'point_of_sale'],
    'data': [
        'views/pos_config_image_view.xml',
        'views/pos_image_view.xml',
    ],
    'qweb': ['static/src/xml/pos_ticket_view.xml',
             'static/src/xml/pos_screen_image_view.xml'],
    'images': ['static/description/banner.jpg'],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
