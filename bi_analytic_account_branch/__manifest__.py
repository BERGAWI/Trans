# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': "Analytic Account Multi Branch",
    'version': '16.0.0.2',
    'category': 'Accounting',
    'summary': "Multi branch analytic account multi branch for single company multi branch analytic model multi branch analytic plans multi branch accounting analytic entries multiple branch analytic accounts multiple branch management multi company environment",
    'description': ''' 

        Analytic Account Multi Branch Odoo App works for both community and enterprise editions. Users can see branch functionality added to analytic accounts, analytic models and analytic plans. Analytic branch pass to the analytic entries.

    ''',
    'author': 'BrowseInfo',
    "price": 29,
    "currency": 'EUR',
    'website': 'https://www.browseinfo.com',
    'depends': ['base','bi_branch_base','bi_branch_invoice'],
    'data': [
        'views/inherit_analytic_account.xml',
        'views/inherit_analytic_distribution.xml',
        'views/account_move_line_inherit.xml',
        'views/inherit_analyatic_plan.xml',

    ],
    'assets': {
            'web.assets_backend': [
                'bi_analytic_account_branch/static/src/inherit_analytic_distribution.js',
            ]
        },
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'live_test_url': 'https://youtu.be/2qF_0C43DGU',
    "images": ['static/description/Analytic-Account-Multi-Branch-Banner.gif'],
}
