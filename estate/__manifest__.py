# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'estate',
    'summary': 'Track housing information',
    'data':[
        "security/security.xml",
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/estate_property.xml',
        'views/property_type.xml',
        'views/property_tag.xml',
        'views/estate_property_offer.xml',
        'views/estate_inherited_models.xml',
        'report/estate_report.xml',
        'report/offer_report.xml',
        'report/report.xml',
    ],
    'category': 'Manufacturing/estate',
    'depends': [
        'base'
    ],
    'application': True,
    'license': 'LGPL-3'

}