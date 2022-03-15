# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2021-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
{
    'name': 'Project Report XLS & PDF',
    'version': '15.0.1.0.0',
    "category": "Project",
    'author': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'maintainer': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'summary': """Advanced PDF & XLS Reports for Project With Filtrations""",
    'description': """Advanced PDF & XLS Reports for Project With Filtrations, Odoo 15, Odoo15""",
    'depends': ['base', 'project'],
    'license': 'AGPL-3',
    'data': ['security/ir.model.access.csv',
             'wizard/project_report_wizard_view.xml',
             'report/project_report_pdf_view.xml',
             'views/project_report_button.xml',
             'views/project_report.xml'
             ],
    'assets': {
            'web.assets_backend': [
                'project_report_pdf/static/src/js/action_manager.js',
            ],
    },
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
}
