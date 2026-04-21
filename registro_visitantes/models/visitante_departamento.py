from odoo import models, fields

class VisitanteDepartamento(models.Model):
    _name = 'registro.visitante.departamento'
    _description = 'Departamentos de Visita'

    name = fields.Char(string='Nombre del Departamento', required=True)
    active = fields.Boolean(default=True, string='Activo')
