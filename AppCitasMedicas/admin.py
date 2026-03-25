from django.contrib import admin
from .models import Paciente, Medico, CitaMedica, Recordatorio, disponibilidad

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre', 'correo', 'telefono')
    search_fields = ('cedula', 'nombre', 'correo')

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ['get_nombre_completo', 'especialidad']
    
    def get_nombre_completo(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_nombre_completo.short_description = "Nombre"

@admin.register(CitaMedica)
class CitaMedicaAdmin(admin.ModelAdmin):
    list_display = ['id_cita', 'paciente', 'medico', 'fecha_hora_cita', 'estado']
    list_filter = ['estado', 'fecha_hora_cita']

@admin.register(Recordatorio)
class RecordatorioAdmin(admin.ModelAdmin):
    list_display = ['cita', 'fecha_envio_programado', 'medio_envio', 'enviado']
    list_filter = ['medio_envio', 'enviado']

@admin.register(disponibilidad)
class disponibilidadAdmin(admin.ModelAdmin):
    list_display = ['medico', 'fecha', 'hora_inicio', 'hora_fin']
    list_filter = ['fecha']
