# Copyright to The City Law Firm
from odoo import models, fields


class Contact(models.AbstractModel):
    _inherit = 'ir.qweb.field.contact'

    
    
class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    attendance_state = fields.Selection(groups="base.group_user,base.group_portal")
    hours_today = fields.Float(groups="base.group_user,base.group_portal")
    last_attendance_id = fields.Many2one(groups="base.group_user,base.group_portal")
    last_check_in = fields.Datetime(groups="base.group_user,base.group_portal")
    last_check_out = fields.Datetime(groups="base.group_user,base.group_portal")

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    attendance_state = fields.Selection(groups="base.group_user,base.group_portal")
    hours_today = fields.Float(groups="base.group_user,base.group_portal")
    last_attendance_id = fields.Many2one(groups="base.group_user,base.group_portal")
    last_check_in = fields.Datetime(groups="base.group_user,base.group_portal")
    last_check_out = fields.Datetime(groups="base.group_user,base.group_portal")
