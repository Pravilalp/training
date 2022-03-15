import pytz

from odoo import models, fields, api


class EmployeeShift(models.Model):
    _name = 'employee.shift'

    name = fields.Char(string="Name")

    start_time = fields.Float(string='Start time')
    end_time = fields.Float(string='Start time')


class Employee(models.Model):
    _inherit = 'hr.employee'

    shift_id = fields.Many2one('employee.shift', string="shift")


class EmployeeAttendance(models.Model):
    _inherit = 'hr.attendance'

    early = fields.Boolean(string='Early')
    late = fields.Boolean(string='Late')

    @api.constrains('check_in', 'check_out')
    def _check_shift(self):
        start = self.employee_id.shift_id.start_time
        end = self.employee_id.shift_id.end_time

        print("********************")

        result = '{0:02.0f}.{1:02.0f}'.format(*divmod(start * 60, 60))
        result_end = '{0:02.0f}.{1:02.0f}'.format(*divmod(end * 60, 60))
        print(result_end)
        print(int((float(result_end))))
        print((round((float(result_end)) % 2, 2)) * 100)
        user_tz = pytz.timezone(self.env.context.get('tz'))
        
        if self.check_in:
            time_in = (pytz.utc.localize(self.check_in).astimezone(user_tz))
            A = (time_in.time().minute * 60) + (time_in.time().hour * 60 * 60)
            B = (((round((float(result)) % 2, 2)) * 100) * 60) + ((int((float(result)))) * 60 * 60)
            if A > B:
                self.late = True
        if self.check_out:
            time_out = (pytz.utc.localize(self.check_out).astimezone(user_tz))
            print(time_out)
            C = (time_out.time().minute * 60) + (time_out.time().hour * 60 * 60)
            D = (((round((float(result_end)) % 2, 2)) * 100) * 60) + ((int((float(result_end)))) * 60 * 60)
            if C < D:
                self.early = True
