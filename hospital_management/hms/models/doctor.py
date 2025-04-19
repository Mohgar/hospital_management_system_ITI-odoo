from odoo import models, fields, api

class Doctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Hospital Doctor'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    image = fields.Binary(string='Image')
    department_id = fields.Many2one(
        'hms.department',
        string='Department',
        required=True
    )
    patient_ids = fields.Many2many(
        'hms.patient',
        string='Patients'
    )
    # full_name = fields.Char(
    #     string='Full Name',
    #     compute='_compute_full_name',
    #     store=True
    # )
    #
    # @api.depends('first_name', 'last_name')
    # def _compute_full_name(self):
    #     for doctor in self:
    #         doctor.full_name = f"{doctor.first_name} {doctor.last_name}"