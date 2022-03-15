import io
import json

from odoo import fields, models
from odoo.tools import date_utils

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class TravelManagementReport(models.TransientModel):
    _name = "report.wizard"
    _description = "Travel management report"

    customer_id = fields.Many2one('res.partner', string='Customer', index=True)
    travel_start_date = fields.Date(string="Travel Start Date")
    travel_end_date = fields.Date(string="Travel End Date")

    def action_excel_customer_report(self):
        print("print excel report")
        if self.customer_id:
            if self.travel_start_date:
                if self.travel_end_date:
                    print("111111111111111111")
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                            ON customer_location.id = travel_customer.source_id
                                            WHERE customer_id = '%s' AND
                                            (travel_start_date >= '%s'
                                            AND travel_end_date <= '%s'
                                            ) """ % (
                        self.customer_id.id, self.travel_start_date, self.travel_end_date,
                    ))
                    source = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                            ON customer_location.id = travel_customer.destination_id
                                            WHERE customer_id = '%s' AND
                                            (travel_start_date >= '%s'
                                            AND travel_end_date <= '%s'
                                            )
                                            """ % (
                        self.customer_id.id, self.travel_start_date, self.travel_end_date,
                    ))
                    destination = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT service FROM travel_customer WHERE customer_id = '%s' AND
                                           (travel_start_date >= '%s'
                                           AND travel_end_date <= '%s'
                                           )
                                          """ % (
                        self.customer_id.id, self.travel_start_date, self.travel_end_date,
                    ))
                    service = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT state FROM travel_customer WHERE customer_id = '%s' AND
                                           (travel_start_date >= '%s'
                                           AND travel_end_date <= '%s'
                                           )""" % (
                        self.customer_id.id, self.travel_start_date, self.travel_end_date,
                    ))
                    state = self.env.cr.fetchall()

                else:
                    print("2222222222222")
                    if self.travel_start_date:
                        self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                                    ON customer_location.id = travel_customer.source_id
                                                                    WHERE customer_id = '%s' AND
                                                                    travel_start_date >= '%s' """ %
                                            (self.customer_id.id, self.travel_start_date
                                             ))
                        source = self.env.cr.fetchall()
                        self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                                    ON customer_location.id = travel_customer.destination_id
                                                                    WHERE customer_id = '%s' AND
                                                                    travel_start_date >= '%s'
                                                                    """ % (
                            self.customer_id.id, self.travel_start_date
                        ))
                        destination = self.env.cr.fetchall()
                        self.env.cr.execute("""SELECT service FROM travel_customer WHERE travel_start_date >= '%s'
                                                                  """ % (
                            self.travel_start_date
                        ))
                        service = self.env.cr.fetchall()
                        self.env.cr.execute("""SELECT state FROM travel_customer WHERE 
                                                customer_id = '%s' AND travel_start_date >= '%s'
                                                                     """ % (
                            self.customer_id.id, self.travel_start_date
                        ))
                        state = self.env.cr.fetchall()

            else:
                print("3333333333333333")
                if self.travel_end_date and self.customer_id:
                    print("121212121212121212")
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                            ON customer_location.id = travel_customer.source_id
                                                            WHERE customer_id = '%s' AND
                                                            travel_end_date <= '%s'
                                                            """ % (
                        self.customer_id.id, self.travel_end_date,
                    ))
                    source = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                            ON customer_location.id = travel_customer.destination_id
                                                             WHERE customer_id = '%s' AND
                                                            travel_end_date <= '%s'
                                                            """ % (
                        self.customer_id.id, self.travel_end_date,
                    ))
                    destination = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT service FROM travel_customer WHERE customer_id = '%s' AND
                                                            travel_end_date <= '%s'
                                                          """ % (
                        self.customer_id.id, self.travel_end_date,
                    ))
                    service = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT state FROM travel_customer  WHERE customer_id = '%s' AND
                                                            travel_end_date <= '%s'
                                                           """ % (
                        self.customer_id.id, self.travel_end_date,
                    ))
                    state = self.env.cr.fetchall()
                elif self.travel_end_date:
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                            ON customer_location.id = travel_customer.source_id
                                                            WHERE
                                                            travel_end_date <= '%s'
                                                            """ % (
                        self.travel_end_date,
                    ))
                    source = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                            ON customer_location.id = travel_customer.destination_id
                                                             WHERE
                                                            travel_end_date <= '%s'
                                                            """ % (
                        self.travel_end_date,
                    ))
                    destination = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT service FROM travel_customer WHERE
                                                            travel_end_date <= '%s'
                                                          """ % (
                        self.travel_end_date,
                    ))
                    service = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT state FROM travel_customer  WHERE
                                                            travel_end_date <= '%s'
                                                           """ % (
                        self.travel_end_date,
                    ))
                    state = self.env.cr.fetchall()

                else:
                    print("lllllllllllllllllllllll")
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                                                                                ON customer_location.id = travel_customer.source_id
                                                                                                                WHERE
                                                                                                                customer_id = '%s' """ %
                                        (self.customer_id.id
                                         ))
                    source = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                                                                                ON customer_location.id = travel_customer.destination_id
                                                                                                                WHERE customer_id = '%s'
                                                                                                                """ % (
                        self.customer_id.id
                    ))
                    destination = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT service FROM travel_customer WHERE customer_id = '%s'
                                                                                                              """ % (
                        self.customer_id.id
                    ))
                    service = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT state FROM travel_customer WHERE customer_id = '%s'
                                                                                                                 """ % (
                        self.customer_id.id
                    ))
                    state = self.env.cr.fetchall()
        else:
            print("44444444444444444444")
            if self.travel_start_date and self.travel_end_date:
                self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                    ON customer_location.id = travel_customer.source_id
                                                    WHERE
                                                    (travel_start_date >= '%s'
                                                    AND travel_end_date <= '%s'
                                                    ) """ % (
                    self.travel_start_date, self.travel_end_date,
                ))
                source = self.env.cr.fetchall()
                self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                    ON customer_location.id = travel_customer.destination_id
                                                    WHERE
                                                    (travel_start_date >= '%s'
                                                    AND travel_end_date <= '%s'
                                                    )
                                                    """ % (
                    self.travel_start_date, self.travel_end_date,
                ))
                destination = self.env.cr.fetchall()
                self.env.cr.execute("""SELECT service FROM travel_customer WHERE
                                                   (travel_start_date >= '%s'
                                                   AND travel_end_date <= '%s'
                                                   )
                                                  """ % (
                    self.travel_start_date, self.travel_end_date,
                ))
                service = self.env.cr.fetchall()
                self.env.cr.execute("""SELECT state FROM travel_customer WHERE
                                                   (travel_start_date >= '%s'
                                                   AND travel_end_date <= '%s'
                                                   )""" % (
                    self.travel_start_date, self.travel_end_date,
                ))
                state = self.env.cr.fetchall()
            elif self.travel_start_date:
                if self.travel_start_date:
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                                                ON customer_location.id = travel_customer.source_id
                                                                                WHERE
                                                                                travel_start_date >= '%s'
                                                                                """ % (
                        self.travel_start_date,
                    ))
                    source = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                                                ON customer_location.id = travel_customer.destination_id
                                                                                 WHERE
                                                                                travel_start_date >= '%s'
                                                                                """ % (
                        self.travel_start_date,
                    ))
                    destination = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT service FROM travel_customer WHERE
                                                                                travel_start_date >= '%s'
                                                                              """ % (
                        self.travel_start_date,
                    ))
                    service = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT state FROM travel_customer  WHERE
                                                                                travel_start_date >= '%s'
                                                                               """ % (
                        self.travel_start_date,
                    ))
                    state = self.env.cr.fetchall()
            elif self.travel_end_date:
                if self.travel_end_date:
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                                                ON customer_location.id = travel_customer.source_id
                                                                                WHERE
                                                                                travel_end_date <= '%s'
                                                                                """ % (
                        self.travel_end_date,
                    ))
                    source = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                                                ON customer_location.id = travel_customer.destination_id
                                                                                 WHERE
                                                                                travel_end_date <= '%s'
                                                                                """ % (
                        self.travel_end_date,
                    ))
                    destination = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT service FROM travel_customer WHERE
                                                                                travel_end_date <= '%s'
                                                                              """ % (
                        self.travel_end_date,
                    ))
                    service = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT state FROM travel_customer  WHERE
                                                                                travel_end_date <= '%s'
                                                                               """ % (
                        self.travel_end_date,
                    ))
                    state = self.env.cr.fetchall()
            else:
                self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                         ON customer_location.id = travel_customer.source_id""")
                source = self.env.cr.fetchall()
                self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                        ON customer_location.id = travel_customer.destination_id""")
                destination = self.env.cr.fetchall()
                self.env.cr.execute("""SELECT service FROM travel_customer """)
                service = self.env.cr.fetchall()
                self.env.cr.execute("""SELECT state FROM travel_customer""")
                state = self.env.cr.fetchall()
        record = list(map(lambda a, b, c, d: (a, b, c, d), source, destination, service, state))

        print(record)
        data = {
            'start_date': self.travel_start_date,
            'end_date': self.travel_end_date,
            'customer': self.customer_id.name,
            'record': record,

        }
        print("*******************************")
        print(data)

        return {
            'type': 'ir.actions.report',
            'data': {'model': 'report.wizard',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Travel Management Report',
                     },
            'report_type': 'xlsx'
        }

    def get_xlsx_report(self, data, response):
        print("Print excel ")
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        user_obj = self.env.user
        sheet = workbook.add_worksheet()  # create a new Excel workbook
        bold = workbook.add_format({'bold': True})
        sheet.set_column('B:K', 20)  # sets the column width
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'bold': True})
        format5 = workbook.add_format({'font_size': 10, 'bg_color': '#FFFFFF'})
        format7 = workbook.add_format({'font_size': 10, 'bg_color': '#FFFFFF'})
        sheet.merge_range('A1:B1', user_obj.company_id.name, format5)
        sheet.merge_range('A2:B2', user_obj.company_id.street, format5)
        sheet.write('A3', user_obj.company_id.city, format5)
        sheet.write('B3', user_obj.company_id.zip, format5)
        sheet.merge_range('A4:B4', user_obj.company_id.state_id.name, format5)
        sheet.merge_range('A5:B5', user_obj.company_id.country_id.name, format5)
        sheet.merge_range('B3:F4', 'TRAVEL MANAGEMENT REPORT', head)
        cell_format = workbook.add_format({'font_size': '12px', 'align': 'center', 'bold': True})
        sheet.write('B7', 'From:', cell_format)
        sheet.merge_range('C7:D7', data['start_date'], txt)
        sheet.write('E7', 'To:', cell_format)
        sheet.merge_range('F7:G7', data['end_date'], txt)

        if data['customer']:
            sheet.write('B8', 'Customer:', cell_format)
            sheet.merge_range('C8:D8', data['customer'], txt)
            print('aaaaaaaaaaaaaaaaaa')
            row = 0
            col = 10
            sheet.write(col, row + 1, 'Sl_No', bold)
            sheet.write(col, row + 2, 'Source Location', bold)
            sheet.write(col, row + 3, 'Destination Location', bold)
            sheet.write(col, row + 4, 'Vehicle', bold)
            sheet.write(col, row + 5, 'state', bold)
            Sl_No = 0
            for rec in data['record']:
                A = sum(rec, [])
                col += 1
                Sl_No += 1
                sheet.write(col, row + 1, Sl_No)
                sheet.write(col, row + 2, A[0])
                sheet.write(col, row + 3, A[1])
                sheet.write(col, row + 4, A[2])
                sheet.write(col, row + 5, A[3])
            col += 3
            sheet.merge_range(col, 0, col, 1, user_obj.company_id.phone, format7)
            sheet.merge_range(col, 2, col, 4, user_obj.company_id.email, format7)
            sheet.merge_range(col, 5, col, 7, user_obj.company_id.website, format7)

        else:
            print('aaaaaaaaaaaaaaaaaa')
            row = 0
            col = 10
            sheet.write(col, row + 1, 'Sl_No', bold)
            sheet.write(col, row + 2, 'Source Location', bold)
            sheet.write(col, row + 3, 'Destination Location', bold)
            sheet.write(col, row + 4, 'Vehicle', bold)
            sheet.write(col, row + 5, 'state', bold)
            Sl_No = 0
            for rec in data['record']:
                A = sum(rec, [])
                col += 1
                Sl_No += 1
                sheet.write(col, row + 1, Sl_No)
                sheet.write(col, row + 2, A[0])
                sheet.write(col, row + 3, A[1])
                sheet.write(col, row + 4, A[2])
                sheet.write(col, row + 5, A[3])
            col += 3
            sheet.merge_range(col, 0, col, 1, user_obj.company_id.phone, format7)
            sheet.merge_range(col, 2, col, 4, user_obj.company_id.email, format7)
            sheet.merge_range(col, 5, col, 7, user_obj.company_id.website, format7)

        workbook.close()
        output.seek(0)  # Move file pointer to the beginning of a File
        response.stream.write(output.read())
        output.close()

    def action_travel_customer_report(self):
        if self.customer_id:
            if self.travel_start_date:
                if self.travel_end_date:
                    print("111111111111111111")
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                            ON customer_location.id = travel_customer.source_id
                                            WHERE customer_id = '%s' AND
                                            (travel_start_date >= '%s'
                                            AND travel_end_date <= '%s'
                                            ) """ % (
                        self.customer_id.id, self.travel_start_date, self.travel_end_date,
                    ))
                    source = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                            ON customer_location.id = travel_customer.destination_id
                                            WHERE customer_id = '%s' AND
                                            (travel_start_date >= '%s'
                                            AND travel_end_date <= '%s'
                                            )
                                            """ % (
                        self.customer_id.id, self.travel_start_date, self.travel_end_date,
                    ))
                    destination = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT service FROM travel_customer WHERE customer_id = '%s' AND
                                           (travel_start_date >= '%s'
                                           AND travel_end_date <= '%s'
                                           )
                                          """ % (
                        self.customer_id.id, self.travel_start_date, self.travel_end_date,
                    ))
                    service = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT state FROM travel_customer WHERE customer_id = '%s' AND
                                           (travel_start_date >= '%s'
                                           AND travel_end_date <= '%s'
                                           )""" % (
                        self.customer_id.id, self.travel_start_date, self.travel_end_date,
                    ))
                    state = self.env.cr.fetchall()

                else:
                    print("2222222222222")
                    if self.travel_start_date:
                        self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                                    ON customer_location.id = travel_customer.source_id
                                                                    WHERE customer_id = '%s' AND
                                                                    travel_start_date >= '%s' """ %
                                            (self.customer_id.id, self.travel_start_date
                                             ))
                        source = self.env.cr.fetchall()
                        self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                                    ON customer_location.id = travel_customer.destination_id
                                                                    WHERE customer_id = '%s' AND
                                                                    travel_start_date >= '%s'
                                                                    """ % (
                            self.customer_id.id, self.travel_start_date
                        ))
                        destination = self.env.cr.fetchall()
                        self.env.cr.execute("""SELECT service FROM travel_customer WHERE travel_start_date >= '%s'
                                                                  """ % (
                            self.travel_start_date
                        ))
                        service = self.env.cr.fetchall()
                        self.env.cr.execute("""SELECT state FROM travel_customer WHERE 
                                                customer_id = '%s' AND travel_start_date >= '%s'
                                                                     """ % (
                            self.customer_id.id, self.travel_start_date
                        ))
                        state = self.env.cr.fetchall()

            else:
                print("3333333333333333")
                if self.travel_end_date and self.customer_id:
                    print("121212121212121212")
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                            ON customer_location.id = travel_customer.source_id
                                                            WHERE customer_id = '%s' AND
                                                            travel_end_date <= '%s'
                                                            """ % (
                        self.customer_id.id, self.travel_end_date,
                    ))
                    source = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                            ON customer_location.id = travel_customer.destination_id
                                                             WHERE customer_id = '%s' AND
                                                            travel_end_date <= '%s'
                                                            """ % (
                        self.customer_id.id, self.travel_end_date,
                    ))
                    destination = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT service FROM travel_customer WHERE customer_id = '%s' AND
                                                            travel_end_date <= '%s'
                                                          """ % (
                        self.customer_id.id, self.travel_end_date,
                    ))
                    service = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT state FROM travel_customer  WHERE customer_id = '%s' AND
                                                            travel_end_date <= '%s'
                                                           """ % (
                        self.customer_id.id, self.travel_end_date,
                    ))
                    state = self.env.cr.fetchall()
                elif self.travel_end_date:
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                            ON customer_location.id = travel_customer.source_id
                                                            WHERE
                                                            travel_end_date <= '%s'
                                                            """ % (
                        self.travel_end_date,
                    ))
                    source = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                            ON customer_location.id = travel_customer.destination_id
                                                             WHERE
                                                            travel_end_date <= '%s'
                                                            """ % (
                        self.travel_end_date,
                    ))
                    destination = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT service FROM travel_customer WHERE
                                                            travel_end_date <= '%s'
                                                          """ % (
                        self.travel_end_date,
                    ))
                    service = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT state FROM travel_customer  WHERE
                                                            travel_end_date <= '%s'
                                                           """ % (
                        self.travel_end_date,
                    ))
                    state = self.env.cr.fetchall()

                else:
                    print("lllllllllllllllllllllll")
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                                                                                ON customer_location.id = travel_customer.source_id
                                                                                                                WHERE
                                                                                                                customer_id = '%s' """ %
                                        (self.customer_id.id
                                         ))
                    source = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                                                                                ON customer_location.id = travel_customer.destination_id
                                                                                                                WHERE customer_id = '%s'
                                                                                                                """ % (
                        self.customer_id.id
                    ))
                    destination = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT service FROM travel_customer WHERE customer_id = '%s'
                                                                                                              """ % (
                        self.customer_id.id
                    ))
                    service = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT state FROM travel_customer WHERE customer_id = '%s'
                                                                                                                 """ % (
                        self.customer_id.id
                    ))
                    state = self.env.cr.fetchall()
        else:
            print("44444444444444444444")
            if self.travel_start_date and self.travel_end_date:
                self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                    ON customer_location.id = travel_customer.source_id
                                                    WHERE
                                                    (travel_start_date >= '%s'
                                                    AND travel_end_date <= '%s'
                                                    ) """ % (
                    self.travel_start_date, self.travel_end_date,
                ))
                source = self.env.cr.fetchall()
                self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                    ON customer_location.id = travel_customer.destination_id
                                                    WHERE
                                                    (travel_start_date >= '%s'
                                                    AND travel_end_date <= '%s'
                                                    )
                                                    """ % (
                    self.travel_start_date, self.travel_end_date,
                ))
                destination = self.env.cr.fetchall()
                self.env.cr.execute("""SELECT service FROM travel_customer WHERE
                                                   (travel_start_date >= '%s'
                                                   AND travel_end_date <= '%s'
                                                   )
                                                  """ % (
                    self.travel_start_date, self.travel_end_date,
                ))
                service = self.env.cr.fetchall()
                self.env.cr.execute("""SELECT state FROM travel_customer WHERE
                                                   (travel_start_date >= '%s'
                                                   AND travel_end_date <= '%s'
                                                   )""" % (
                    self.travel_start_date, self.travel_end_date,
                ))
                state = self.env.cr.fetchall()
            elif self.travel_start_date:
                if self.travel_start_date:
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                                                ON customer_location.id = travel_customer.source_id
                                                                                WHERE
                                                                                travel_start_date >= '%s'
                                                                                """ % (
                        self.travel_start_date,
                    ))
                    source = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                                                ON customer_location.id = travel_customer.destination_id
                                                                                 WHERE
                                                                                travel_start_date >= '%s'
                                                                                """ % (
                        self.travel_start_date,
                    ))
                    destination = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT service FROM travel_customer WHERE
                                                                                travel_start_date >= '%s'
                                                                              """ % (
                        self.travel_start_date,
                    ))
                    service = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT state FROM travel_customer  WHERE
                                                                                travel_start_date >= '%s'
                                                                               """ % (
                        self.travel_start_date,
                    ))
                    state = self.env.cr.fetchall()
            elif self.travel_end_date:
                if self.travel_end_date:
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                                                ON customer_location.id = travel_customer.source_id
                                                                                WHERE
                                                                                travel_end_date <= '%s'
                                                                                """ % (
                        self.travel_end_date,
                    ))
                    source = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                                                                ON customer_location.id = travel_customer.destination_id
                                                                                 WHERE
                                                                                travel_end_date <= '%s'
                                                                                """ % (
                        self.travel_end_date,
                    ))
                    destination = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT service FROM travel_customer WHERE
                                                                                travel_end_date <= '%s'
                                                                              """ % (
                        self.travel_end_date,
                    ))
                    service = self.env.cr.fetchall()
                    self.env.cr.execute("""SELECT state FROM travel_customer  WHERE
                                                                                travel_end_date <= '%s'
                                                                               """ % (
                        self.travel_end_date,
                    ))
                    state = self.env.cr.fetchall()
            else:
                self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                         ON customer_location.id = travel_customer.source_id""")
                source = self.env.cr.fetchall()
                self.env.cr.execute("""SELECT city FROM customer_location INNER JOIN travel_customer
                                        ON customer_location.id = travel_customer.destination_id""")
                destination = self.env.cr.fetchall()
                self.env.cr.execute("""SELECT service FROM travel_customer """)
                service = self.env.cr.fetchall()
                self.env.cr.execute("""SELECT state FROM travel_customer""")
                state = self.env.cr.fetchall()

        record = list(map(lambda a, b, c, d: (a, b, c, d), source, destination, service, state))
        # print(record)
        data = {
            'form': self.read()[0],
            'record': record,
        }
        return self.env.ref('travel_management.action_report_travel_customer_details').report_action(self, data=data)
