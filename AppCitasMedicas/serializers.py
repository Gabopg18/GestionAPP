from rest_framework import serializers
from .models import disponibilidad, CitaMedica, Medico, Paciente

class MedicoSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Medico
        fields = ['id', 'nombre_completo', 'especialidad']

    def get_nombre_completo(self, obj):
        full_name = obj.user.get_full_name()
        return full_name if full_name else obj.user.username

class DisponibilidadSerializer(serializers.ModelSerializer):
    medico_nombre = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()

    class Meta:
        model = disponibilidad
        fields = ['id', 'medico', 'medico_nombre', 'fecha', 'hora_inicio', 'hora_fin', 'color']

    def get_medico_nombre(self, obj):
        full_name = obj.medico.user.get_full_name()
        return full_name if full_name else obj.medico.user.username

    def get_color(self, obj):
        # Lógica de colores premium para FullCalendar
        return "#28a745" # Verde por defecto (Disponible)

class CitaMedicaSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.ReadOnlyField(source='paciente.nombre')
    medico_nombre = serializers.ReadOnlyField(source='medico.user.get_full_name')

    class Meta:
        model = CitaMedica
        fields = '__all__'
