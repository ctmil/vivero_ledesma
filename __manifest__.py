# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
'name': 'Vivero Ledesma',
'version': '1.0',
'category': 'Tools',
'summary': 'Vivero Ledesma',
'depends': ['web','sale','product','base'],
'data': [
    'security/ir.model.access.csv',
    'vivero_view.xml',
],
'demo': [
    #'data/demo.xml',
    #'security/ir.model.access.csv',
],
'css': [],
'installable': True,
'auto_install': False,
'application': True,
}
