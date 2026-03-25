from django.db import models
from django.contrib.auth.models import User
import uuid # Para IDCita, si prefieres UUIDs

class Paciente(models.Model):
    cedula = models.CharField(max_length=20, primary_key=True, verbose_name="Cédula")
    nombre = models.CharField(max_length=100, verbose_name="Nombre Completo")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")
    direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dirección")
    correo = models.EmailField(verbose_name="Correo Electrónico")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

class Medico(models.Model):
    # Usamos el User de Django para autenticación (nombre, correo, contraseña)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name="Usuario")
    especialidad = models.CharField(max_length=100, verbose_name="Especialidad")


    def __str__(self):
        return f"Dr(a). {self.user.get_full_name() or self.user.username} - {self.especialidad}"

    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"

class disponibilidad(models.Model):
    """
    Representa un bloque de tiempo en el que un médico está disponible.
    Un médico puede tener muchos horarios disponibles.
    Una cita se puede agendar en uno de estos horarios.
    """
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name="disponibilidad")
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()


    def __str__(self):
        return f"{self.medico} - {self.fecha} ({self.hora_inicio} - {self.hora_fin})"

    class Meta:
        verbose_name = "disponibilidad"
        verbose_name_plural = "disponibilidades"
        unique_together = ('medico', 'fecha', 'hora_inicio') # Evitar duplicados

class CitaMedica(models.Model):
    ESTADO_CHOICES = [
        ('Agendada', 'Agendada'),
        ('Confirmada', 'Confirmada'), 
        ('Cancelada_Paciente', 'Cancelada por Paciente'),
        ('Cancelada_Medico', 'Cancelada por Médico'),
        ('Realizada', 'Realizada'),
        ('No_Asistio', 'No Asistió'),
    ]

    # IDCita podría ser el ID automático de Django, o un UUID
    id_cita = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID Cita")
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name="citas", verbose_name="Paciente") # PROTECT para no borrar paciente si tiene citas
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT, related_name="citas", verbose_name="Médico")

    fecha_hora_cita = models.DateTimeField(verbose_name="Fecha y Hora de la Cita")
    # duracion_minutos = models.IntegerField(default=30, verbose_name="Duración (minutos)") # Opcional si las citas tienen duración variable
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Agendada', verbose_name="Estado")
    # InfoPaciente e InfoMedico del diagrama pueden ser notas:
    notas_paciente = models.TextField(blank=True, null=True, verbose_name="Notas del Paciente (ej. motivo)")
    notas_adicionales_medico = models.TextField(blank=True, null=True, verbose_name="Notas Adicionales del Médico")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Cita {self.id_cita} - {self.paciente} con {self.medico} el {self.fecha_hora_cita.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Cita Médica"
        verbose_name_plural = "Citas Médicas"
        ordering = ['fecha_hora_cita']

class Recordatorio(models.Model):
    MEDIO_CHOICES = [
        ('Email', 'Correo Electrónico'),
        ('SMS', 'SMS'), # Implementar SMS requiere un servicio externo
    ]
    cita = models.ForeignKey(CitaMedica, on_delete=models.CASCADE, related_name="recordatorios", verbose_name="Cita")
    fecha_envio_programado = models.DateTimeField(verbose_name="Fecha de Envío Programado")
    medio_envio = models.CharField(max_length=10, choices=MEDIO_CHOICES, verbose_name="Medio de Envío")
    enviado = models.BooleanField(default=False, verbose_name="¿Enviado?")
    fecha_enviado = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Envío Real")

    def __str__(self):
        return f"Recordatorio para cita {self.cita.id_cita} por {self.medio_envio} ({'Enviado' if self.enviado else 'Pendiente'})"

    class Meta:
        verbose_name = "Recordatorio"
        verbose_name_plural = "Recordatorios"

