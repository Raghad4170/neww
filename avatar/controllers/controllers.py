# Copyright to The City Law Firm
import base64

from odoo.http import content_disposition, Controller, request, route
import odoo.addons.portal.controllers.portal as PortalController
from odoo import exceptions
import datetime
from odoo import http, _
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError
import requests



class CustomerPortal(PortalController.CustomerPortal):

    def account(self, redirect=None, **post):
        if 'image_1920' in post:
            image_1920 = post.get('image_1920')
            if image_1920:
                image_1920 = image_1920.read()
                image_1920 = base64.b64encode(image_1920)
                request.env.user.partner_id.sudo().write({
                    'image_1920': image_1920
                })
            post.pop('image_1920')
        if 'clear_avatar' in post:
            request.env.user.partner_id.sudo().write({
                'image_1920': False
            })
            post.pop('clear_avatar')
        return super(CustomerPortal, self).account(redirect=redirect, **post)
    
class MyAttendance(http.Controller):
    
    @http.route(['/my/sign_in_attendance'], type='http', auth="user", website=True)
    def sign_in_attendace(self, **post):
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
        check_in = datetime.now().strftime("%Y-%m-%d %H:%M:%S")        
        if employee:
            just_checked_out = request.env['hr.attendance'].sudo().search([('employee_id','=',employee.id),('check_in', '<', datetime.now()), ('check_out', '<', datetime.now())], order='create_date desc', limit=1)
            if just_checked_out:
                time_check_out_s = datetime.now() - just_checked_out.check_out
                time_check_out = time_check_out_s.total_seconds() / 60
                if time_check_out <= 5:
                    return request.render('avatar.sign_attendance_error', {'time_check_in':'لا يمكنك تسجيل الدخول بعد تسجيل خروجك بأقل من ٥ دقائق'})
                else:
                    vals = {
                            'employee_id': employee.id,
                            'check_in': check_in,
                            }
                    attendance = request.env['hr.attendance'].sudo().create(vals)
            else:
                vals = {
                        'employee_id': employee.id,
                        'check_in': check_in,
                        }
                attendance = request.env['hr.attendance'].sudo().create(vals)
        return request.redirect('/my')


    @http.route(['/my/sign_out_attendance'], type='http', auth="user", website=True)
    def sign_out_attendace(self, **post):
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
        if employee:
            just_checked_in = request.env['hr.attendance'].sudo().search([('employee_id','=',employee.id),('check_in', '<', datetime.now()), ('check_in', '>', datetime.strptime(date.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))], order='create_date desc',limit=1)
            if just_checked_in:
                time_check_in_s = datetime.now() - just_checked_in.check_in
                time_check_in = time_check_in_s.total_seconds() / 60
                if time_check_in <= 5:
                    return request.render('avatar.sign_attendance_error', {'time_check_in':'لا يمكنك تسجيل الخروج بعد تسجيل دخولك بأقل من ٥ دقائق'})
                else:
                    no_check_out_attendances = request.env['hr.attendance'].search([
                                ('employee_id', '=', employee.id),
                                ('check_out', '=', False),
                            ])
                    check_out = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
                    attendance = no_check_out_attendances.write({'check_out':check_out})
            else:
                no_check_out_attendances = request.env['hr.attendance'].search([
                            ('employee_id', '=', employee.id),
                            ('check_out', '=', False),
                        ])
                check_out = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
                attendance = no_check_out_attendances.write({'check_out':check_out})
        return request.redirect('/my')

