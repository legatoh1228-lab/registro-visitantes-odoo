from odoo import models, fields

class VisitantePerfil(models.Model):
    _name = 'visitante.perfil'
    _description = 'Directorio de Perfiles de Visitantes'
    _rec_names_search = ['visitante_nombre', 'documento']

    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.tipo_documento}-{record.documento} {record.visitante_nombre}"

    visitante_nombre = fields.Char(string='Nombre del Visitante', required=True)
    tipo_documento = fields.Selection([
        ('V', 'Venezolano'), ('E', 'Extranjero'),
        ('J', 'Jurídico'), ('G', 'Gubernamental'), ('P', 'Pasaporte')
    ], string='Tipo de Doc.', default='V', required=True)
    documento = fields.Char(string='Núm. de Documento', required=True)
    
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento")
    empresa_procedencia = fields.Char(string='Empresa / Institución')
    especialidad_id = fields.Many2one('registro.visitante.especialidad', string="Especialidad")
    image_1920 = fields.Image(string="Fotografía")
    
    _sql_constraints = [
        ('doc_unico', 'unique (tipo_documento, documento)', 'Ya existe un perfil guardado con este tipo y número de documento.')
    ]
