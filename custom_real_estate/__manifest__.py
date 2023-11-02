# -*- coding: utf-8 -*-
{
    'name': "Real Estate",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Syncoria",
    'website': "https://www.syncoria.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Construction',
    'version': '16.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/menu.xml',
        'views/properties.xml',
        'views/property_type.xml',
        'views/property_tag.xml',
        'views/property_offer.xml',
        # 'views/property_task.xml',
        # 'views/date_range.xml',
        # 'views/task.xml',
        # 'views/range.xml',
        'views/date_task.xml',
        'views/generate_date_range.xml',
        'report/property_report.xml',
        'report/report.xml'
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    'license': 'LGPL-3',
}
