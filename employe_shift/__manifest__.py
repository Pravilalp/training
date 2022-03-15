{
    'name': 'Employee Shift',
    'version': '15.0.1.0.0',
    'summary': 'Employee Shift',
    'sequence': -200,
    'description': "Employee Shift",
    'category': '',
    'website': '',
    'data': ['security/ir.model.access.csv',
             'views/shift.xml'

             ],
    'depends': ['base', 'hr', 'hr_attendance'],

    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
