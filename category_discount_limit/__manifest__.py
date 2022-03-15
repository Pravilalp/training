{
    'name': 'POS Category Discount Limit',
    'version': '15.0.1.0.0',
    'summary': 'POS Category Discount Limit',
    'sequence': -200,
    'description': "POS Category Discount Limit",
    'category': '',
    'website': '',
    'data': ['views/discount_limit.xml'
             ],
    'depends': ['base', 'point_of_sale'],
    'assets': {
        'web.assets_backend': [
            '/category_discount_limit/static/src/js/discount_limit.js',
        ],
    },
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
