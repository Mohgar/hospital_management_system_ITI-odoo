from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'
    _inherit = ['mail.thread']

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    birth_date = fields.Date(string='Birth Date')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    email = fields.Char(string='Email', unique=True)
    blood_type = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'),
    ], string='Blood Type')
    pcr = fields.Boolean(string='PCR')
    cr_ratio = fields.Float(string='CR Ratio')
    image = fields.Binary(string='Image')
    history = fields.Html(string='History')
    address = fields.Text(string='Address')
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], string='State', default='undetermined', tracking=True)
    department_id = fields.Many2one(
        'hms.department',
        string='Department',
        domain="[('is_opened', '=', True)]"
    )
    doctor_ids = fields.Many2many(
        'hms.doctor',
        string='Doctors',
        compute='_compute_doctor_ids',
        inverse='_inverse_doctor_ids',
        store=True,
        readonly=False
    )
    log_history_ids = fields.One2many(
        'hms.log.history',
        'patient_id',
        string='Log History'
    )
    related_customer_id = fields.Many2one(
        'res.partner',
        string='Related Customer',
        domain="[('is_company', '=', False)]"
    )
    department_capacity = fields.Integer(
        string='Department Capacity',
        related='department_id.capacity',
        readonly=True
    )

    def _inverse_doctor_ids(self):
        """
        Required for computed writable field.
        We don't need to implement anything here as we're using compute only
        """
        pass
    @api.depends('department_id')
    def _compute_doctor_ids(self):
        for patient in self:
            if not patient.department_id:
                patient.doctor_ids = False
            else:
                # Get doctors from the selected department
                doctors = self.env['hms.doctor'].search([
                    ('department_id', '=', patient.department_id.id)
                ])
                patient.doctor_ids = doctors



    @api.depends('birth_date')
    def _compute_age(self):
        today = fields.Date.today()
        for patient in self:
            if patient.birth_date:
                delta = today - patient.birth_date
                patient.age = delta.days // 365
            else:
                patient.age = 0

    @api.onchange('birth_date')
    def _onchange_birth_date(self):
        if self.birth_date:
            today = fields.Date.today()
            delta = today - self.birth_date
            self.age = delta.days // 365
            if self.age < 30 and not self.pcr:
                self.pcr = True
                return {
                    'warning': {
                        'title': 'PCR Checked',
                        'message': 'PCR has been automatically checked because age is under 30'
                    }
                }

    @api.onchange('pcr')
    def _onchange_pcr(self):
        if self.pcr and not self.cr_ratio:
            return {
                'warning': {
                    'title': 'CR Ratio Required',
                    'message': 'CR Ratio is required when PCR is checked'
                }
            }

    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id and not self.department_id.is_opened:
            self.department_id = False
            return {
                'warning': {
                    'title': 'Closed Department',
                    'message': 'You cannot select a closed department'
                }
            }
        self.doctor_ids = False

    @api.constrains('email')
    def _check_email(self):
        for patient in self:
            if patient.email and not '@' in patient.email:
                raise ValidationError('Please enter a valid email address')

    @api.constrains('pcr', 'cr_ratio')
    def _check_pcr_cr_ratio(self):
        for patient in self:
            if patient.pcr and not patient.cr_ratio:
                raise ValidationError('CR Ratio is required when PCR is checked')

    def write(self, vals):
        if 'state' in vals:
            for patient in self:
                self.env['hms.log.history'].create({
                    'patient_id': patient.id,
                    'description': f'State changed to {vals["state"]}'
                })
        return super(Patient, self).write(vals)