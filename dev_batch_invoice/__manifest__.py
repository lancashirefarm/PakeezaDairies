# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd. (<http://devintellecs.com>).
#
##############################################################################
{
    "name": "Batch Invoice Customer/Suppplier",
    "category": 'Generic Modules/Accounting',
    "summary": """
                  Apps will create a batch invoice of customer and supplier in one click
        """,
    "description": """
        Apps will create a batch invoice of customer and supplier in one click
        
        Batch Invoice, Multiple Invocie, Invoice payment, Multiple Invoice Payment, Bulk invoice Payment, Multi vendor payment, multi invoice payment,  
    """,
    "sequence": 1,
    "author": "DevIntelle Consulting Service Pvt.Ltd",
    "website": "http://www.devintellecs.com",
    'images': ['images/main_screenshot.png'],
    "version": '1.0',
    "depends": ['account'],
    "data": [
        'security/ir.model.access.csv',
        'views/dev_account_invoice_view.xml',
        'views/account_sequence.xml',
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    'price':20.0,
    'currency':'EUR',
    'live_test_url':'https://youtu.be/Kx9DeGn4d6I',     
    
}
