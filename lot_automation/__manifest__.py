# -*- coding: utf-8 -*-
{
    'name': "Lot/Serial Numbers Automation",
    'summary': """This App is used for the automation of lot number""",
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Stock',
    'version': '0.1',
    'depends': ['base', 'stock', 'mrp', ],
    'data': ['views/stock.picking.custom.xml',
             'views/custom_mrp_product_produce_view.xml',
             'views/mrp.prodution.wizard.xml',
             ],
    'demo': ['demo/demo.xml',
             ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
