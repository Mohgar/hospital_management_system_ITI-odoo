from odoo import models, fields, api

class Department(models.Model):
    _name = 'hms.department'
    _description = 'Hospital Department'

    name = fields.Char(string='Name', required=True)
    capacity = fields.Integer(string='Capacity')
    is_opened = fields.Boolean(string='Is Opened', default=True)
    patient_ids = fields.One2many(
        'hms.patient',
        'department_id',
        string='Patients'
    )
    doctor_ids = fields.One2many(
        'hms.doctor',
        'department_id',
        string='Doctors'
    )
    # patient_count = fields.Integer(
    #     string='Patient Count',
    #     compute='_compute_patient_count',
    #     store=True
    # )
    #
    # @api.depends('patient_ids')
    # def _compute_patient_count(self):
    #     for department in self:
    #         department.patient_count = len(department.patient_ids)

    # @api.constrains('capacity', 'patient_ids')
    # def _check_capacity(self):
    #     for department in self:
    #         if department.capacity and len(department.patient_ids) > department.capacity:
    #             raise ValidationError('Department capacity exceeded!')