from odoo import models, fields

class VisitanteEspecialidad(models.Model):
    _name = 'registro.visitante.especialidad'
    _description = 'Especialidad de Visitantes'

    name = fields.Char(string='Especialidad', required=True)
    active = fields.Boolean(default=True, string='Activo')
