{
    'name': 'Travel Management',
    'version': '15.0.1.0.0',
    'summary': 'Travel Management',
    'sequence': -200,
    'description': "Travel management",
    'category': 'Productivity',
    'website': 'https://www.odoo.com/travel',
    'data': ['wizard/travel_customer_report.xml',
             'reports/customer_report.xml',
             'reports/travel_customer_details_report.xml',
             'security/security.xml',
             'security/ir.model.access.csv',
             'data/sequence.xml',
             'data/autoremove.xml',
             'views/customer.xml',
             'views/customer_service_type.xml',
             'views/customer_tour_package.xml',
             'views/customer_vehicle.xml',

             ],
    'depends': ['base', 'mail'],
    'assets': {
        'web.assets_backend': [
            'travel_management/static/src/js/action_manager.js',
        ],
    },
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
