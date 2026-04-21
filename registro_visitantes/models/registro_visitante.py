from odoo import models, fields, api

class RegistroVisitante(models.Model):
    _name = 'registro.visitante'
    _description = 'Registro de Visitantes'

    name = fields.Char(string='Número', required=True, copy=False, readonly=True, default=lambda self: 'Nuevo')
    image_1920 = fields.Image(string="Fotografía")
    
    tipo_registro = fields.Selection([
        ('nuevo', 'Visitante Nuevo'),
        ('recurrente', 'Visitante Recurrente')
    ], string='Tipo de Registro', default='nuevo', required=True)
    
    perfil_id = fields.Many2one('visitante.perfil', string="Buscar Visitante Anterior")
    
    visitante_nombre = fields.Char(string='Nombre completo', required=True)
    tipo_documento = fields.Selection([
        ('V', 'Venezolano (V)'),
        ('E', 'Extranjero (E)'),
        ('J', 'Jurídico (J)'),
        ('G', 'Gubernamental (G)'),
        ('P', 'Pasaporte (P)')
    ], string='Tipo de Doc.', default='V', required=True)
    documento = fields.Char(string='Núm. de Documento', required=True)
    
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento")
    edad = fields.Integer(string="Edad", compute="_compute_edad", store=True, group_operator=False)
    
    empresa_procedencia = fields.Char(string='Empresa / Institución')
    especialidad_id = fields.Many2one('registro.visitante.especialidad', string="Especialidad")
    
    motivo = fields.Char(string='Motivo de la Visita', required=True)
    departamento_id = fields.Many2one('registro.visitante.departamento', string='Departamento a Visitar', required=True)
    gafete = fields.Char(string='Gafete / Pase Asignado', required=True)
    
    placa_vehiculo = fields.Char(string='Placa de Vehículo')
    equipos_ingresados = fields.Text(string='Equipos y Pertenencias', help='Indique laptops, herramientas, u otros objetos ingresados')
    
    fecha_entrada = fields.Datetime(string='Fecha de Entrada', default=fields.Datetime.now)
    fecha_salida = fields.Datetime(string='Fecha de Salida')
    duracion_visita = fields.Char(string="Duración de la Visita", compute="_compute_duracion_visita")
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('proceso', 'En Visita'),
        ('salida', 'Salida')
    ], string='Estado', default='borrador', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code('registro.visitante') or 'Nuevo'
                
            if vals.get('tipo_registro') == 'nuevo':
                PerfilEnv = self.env['visitante.perfil']
                existente = PerfilEnv.search([
                    ('tipo_documento', '=', vals.get('tipo_documento')),
                    ('documento', '=', vals.get('documento'))
                ], limit=1)
                
                if not existente:
                    nuevo_perfil = PerfilEnv.create({
                        'visitante_nombre': vals.get('visitante_nombre'),
                        'tipo_documento': vals.get('tipo_documento'),
                        'documento': vals.get('documento'),
                        'fecha_nacimiento': vals.get('fecha_nacimiento'),
                        'empresa_procedencia': vals.get('empresa_procedencia'),
                        'especialidad_id': vals.get('especialidad_id'),
                        'image_1920': vals.get('image_1920'),
                    })
                    vals['perfil_id'] = nuevo_perfil.id
                else:
                    vals['perfil_id'] = existente.id

        return super().create(vals_list)

    @api.onchange('perfil_id')
    def _onchange_perfil_id(self):
        """Si selecciona visitante recurrente, hereda la data de su perfil maestro maestro."""
        if self.perfil_id:
            record = self.perfil_id
            self.visitante_nombre = record.visitante_nombre
            self.tipo_documento = record.tipo_documento
            self.documento = record.documento
            self.fecha_nacimiento = record.fecha_nacimiento
            self.empresa_procedencia = record.empresa_procedencia
            self.especialidad_id = record.especialidad_id.id if record.especialidad_id else False
            self.image_1920 = record.image_1920
            
            return {
                'warning': {
                    'title': "Visitante Recuperado",
                    'message': f"Se han importado exitosamente los datos de {record.visitante_nombre} desde el Directorio.",
                }
            }

    @api.depends('fecha_nacimiento')
    def _compute_edad(self):
        for record in self:
            if record.fecha_nacimiento:
                today = fields.Date.today()
                record.edad = today.year - record.fecha_nacimiento.year - ((today.month, today.day) < (record.fecha_nacimiento.month, record.fecha_nacimiento.day))
            else:
                record.edad = 0

    def action_iniciar_visita(self):
        for record in self:
            record.estado = 'proceso'

    def action_marcar_salida(self):
        for record in self:
            record.write({'estado': 'salida', 'fecha_salida': fields.Datetime.now()})

    @api.depends('fecha_entrada', 'fecha_salida')
    def _compute_duracion_visita(self):
        for record in self:
            if record.fecha_entrada and record.fecha_salida:
                diff = record.fecha_salida - record.fecha_entrada
                total_seconds = int(diff.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                record.duracion_visita = f"{hours} Hora(s) y {minutes} Minuto(s)"
            else:
                record.duracion_visita = "En Proceso / Sin Finalizar"
