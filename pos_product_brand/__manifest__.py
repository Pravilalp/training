{
    'name': 'POS Product Brand',
    'version': '15.0.1.0.0',
    'summary': 'Pos Product Brand',
    'sequence': -200,
    'description': "Pos Product Brand",
    'category': 'Productivity',
    'website': '',
    'data': ['security/ir.model.access.csv',
             'views/product_brand.xml',

             ],
    'assets': {
        'web.assets_backend': [
            '/pos_product_brand/static/src/js/product_brand.js',
            '/pos_product_brand/static/src/js/brand_receipt.js'

        ],
        'web.assets_qweb': [
            'pos_product_brand/static/src/xml/product_brand.xml',
            '/pos_product_brand/static/src/xml/brand_receipt.xml'

        ],
    },
    'depends': ['base', 'point_of_sale'],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
