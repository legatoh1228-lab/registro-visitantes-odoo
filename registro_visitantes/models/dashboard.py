from odoo import models, fields, api

class VisitorDashboard(models.TransientModel):
    _name = 'registro.visitante.dashboard'
    _description = 'Lobby Principal e Interactivo'

    name = fields.Char(default="Dashboard")

    @api.model
    def action_init_dashboard(self):
        board = self.create({})
        return {
            'name': 'Centro de Mando',
            'type': 'ir.actions.act_window',
            'res_model': 'registro.visitante.dashboard',
            'res_id': board.id,
            'view_mode': 'form',
            'target': 'inline',
        }

    def action_open_nuevas_visitas(self):
        return {
            'name': 'Personal Adentro',
            'type': 'ir.actions.act_window',
            'res_model': 'registro.visitante',
            'view_mode': 'kanban,list,form',
            'domain': "[('estado', '=', 'proceso')]"
        }

    def action_open_crear_visita(self):
        return {
            'name': 'Emisión de Nuevo Pase',
            'type': 'ir.actions.act_window',
            'res_model': 'registro.visitante',
            'view_mode': 'form',
            'target': 'current',
        }

    def action_open_directorio(self):
        return {
            'name': 'Directorio Global',
            'type': 'ir.actions.act_window',
            'res_model': 'visitante.perfil',
            'view_mode': 'kanban,list,form',
        }
        
    def action_open_configuracion(self):
        return {
            'name': 'Opciones de Gestión',
            'type': 'ir.actions.act_window',
            'res_model': 'registro.visitante.gestion.wizard',
            'view_mode': 'form',
            'target': 'new',
        }

    def action_open_estadisticas(self):
        return {
            'name': 'Módulo de Estadísticas',
            'type': 'ir.actions.act_window',
            'res_model': 'registro.visitante.estadisticas.wizard',
            'view_mode': 'form',
            'target': 'new',
        }

class GestionWizard(models.TransientModel):
    _name = 'registro.visitante.gestion.wizard'
    _description = 'Wizard de Gestión'

    def action_open_departamentos(self):
        return {
            'name': 'Departamentos',
            'type': 'ir.actions.act_window',
            'res_model': 'registro.visitante.departamento',
            'view_mode': 'list',
        }

    def action_open_especialidades(self):
        return {
            'name': 'Especialidades',
            'type': 'ir.actions.act_window',
            'res_model': 'registro.visitante.especialidad',
            'view_mode': 'list',
        }

class EstadisticasWizard(models.TransientModel):
    _name = 'registro.visitante.estadisticas.wizard'
    _description = 'Wizard de Estadísticas'

    def action_open_departamento(self):
        return {
            'name': 'Estadísticas por Departamento',
            'type': 'ir.actions.act_window',
            'res_model': 'registro.visitante',
            'view_mode': 'graph,pivot',
            'context': {'search_default_groupby_departamento': 1, 'graph_mode': 'pie'},
        }

    def action_open_especialidad(self):
        return {
            'name': 'Estadísticas por Especialidad',
            'type': 'ir.actions.act_window',
            'res_model': 'registro.visitante',
            'view_mode': 'graph,pivot',
            'context': {'search_default_groupby_especialidad': 1, 'graph_mode': 'pie'},
        }

    def action_open_edad(self):
        return {
            'name': 'Estadísticas por Edad',
            'type': 'ir.actions.act_window',
            'res_model': 'registro.visitante',
            'view_mode': 'graph,pivot',
            'context': {'search_default_groupby_edad': 1, 'graph_mode': 'pie'},
        }
