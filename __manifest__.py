{
    'name': 'Registro de Visitantes',
    'version': '1.0',
    'summary': 'Modulo sencillo para el registro de visitantes',
    'description': 'Permite registrar la entrada y salida de visitantes.',
    'author': 'Tu Nombre',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/dashboard_view.xml',
        'views/visitante_perfil_view.xml',
        'views/registro_visitantes_view.xml',
        'report/visitante_report.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}