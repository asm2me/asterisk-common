# -*- encoding: utf-8 -*-
{
    'name': 'Odoo PBX',
    'version': '1.1',
    'author': 'Odooist',
    'maintainer': 'Odooist',
    'support': 'odooist@gmail.com',
    'license': 'OPL-1',
    'price': 0,
    'currency': 'EUR',
    'category': 'Phone',
    'summary': 'Odoo based enterprise grade IP-PBX application',
    'description': 'Odoo based enterprise grade IP-PBX application',
    'depends': [
        'asterisk_common',
        'asterisk_calls',
        'asterisk_calls_crm',
        'asterisk_base',
        'asterisk_base_sip',
        'asterisk_base_queues',
    ],
    'data': [
    ],
    'demo': [],
    "qweb": ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/Asterisk_Logo.png'],
}
