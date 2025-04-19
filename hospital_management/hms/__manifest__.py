{
    'name': 'Hospitals Management System',
    'version': '1.0',
    'summary': 'Manage hospital departments, doctors and patients',
    'description': """
        Comprehensive hospital management system covering patients,
        departments, doctors and their relationships
    """,
    'author': 'mohamed hgar',
    'category': 'Healthcare',
    'depends': ['base', 'mail', 'crm'],
    'data': [
        'security/security.xml',
        'views/department_views.xml',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/menu_views.xml',
        'report/patient_report.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}