from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid
from django.utils.timezone import now

class DisponibilidadManager(models.Manager):
    """Encapsula consultas frecuentes de disponibilidad"""
    def de_hoy_en_adelante(self, medico):
        return self.filter(medico=medico, fecha__gte=now().date()).order_by('fecha', 'hora_inicio')

class CitaMedicaManager(models.Manager):
    """Encapsula consultas frecuentes de citas"""
    def activas_paciente(self, cedula):
        return self.filter(paciente__cedula=cedula, fecha_hora_cita__date__gte=now().date()).order_by('fecha_hora_cita')

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name="Usuario")
    especialidad = models.CharField(max_length=100, verbose_name="Especialidad")

    def __str__(self):
        return f"Dr(a). {self.user.get_full_name() or self.user.username} - {self.especialidad}"

    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"

class disponibilidad(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name="disponibilidad")
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    objects = DisponibilidadManager()

    def clean(self):
        # Validar que hora_fin sea posterior a hora_inicio
        if self.hora_inicio and self.hora_fin:
            if self.hora_inicio >= self.hora_fin:
                raise ValidationError("La hora de inicio debe ser anterior a la hora de fin.")

        # GES-14: Evitar cruce de horarios en una misma especialidad
        # Buscamos disponibilidades que se solapen en la misma fecha y misma especialidad
        overlaps = disponibilidad.objects.filter(
            medico__especialidad=self.medico.especialidad,
            fecha=self.fecha
        ).exclude(pk=self.pk)

        for overlap in overlaps:
            # Lógica de solapamiento: (StartA < EndB) and (EndA > StartB)
            if (self.hora_inicio < overlap.hora_fin) and (self.hora_fin > overlap.hora_inicio):
                raise ValidationError(
                    f"Cruce de horario detectado: {overlap.medico} ya tiene un horario "
                    f"de {overlap.hora_inicio} a {overlap.hora_fin} para la especialidad {self.medico.especialidad}."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.medico} - {self.fecha} ({self.hora_inicio} - {self.hora_fin})"

    class Meta:
        verbose_name = "disponibilidad"
        verbose_name_plural = "disponibilidades"
        unique_together = ('medico', 'fecha', 'hora_inicio')
        indexes = [
            models.Index(fields=['medico', 'fecha']),
            models.Index(fields=['fecha', 'hora_inicio']),
        ]

class CitaMedica(models.Model):
    # GES-16: Estados definidos: Pendiente, Confirmada, Cancelada
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'), 
        ('Cancelada', 'Cancelada'),
        ('Realizada', 'Realizada'),
        ('No_Asistio', 'No Asistió'),
    ]

    objects = CitaMedicaManager()

    id_cita = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID Cita")
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name="citas", verbose_name="Paciente")
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT, related_name="citas", verbose_name="Médico")

    fecha_hora_cita = models.DateTimeField(verbose_name="Fecha y Hora de la Cita")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente', verbose_name="Estado")
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
        indexes = [
            models.Index(fields=['paciente', 'fecha_hora_cita']),
            models.Index(fields=['medico', 'fecha_hora_cita']),
            models.Index(fields=['estado']),
        ]

class Recordatorio(models.Model):
    MEDIO_CHOICES = [
        ('Email', 'Correo Electrónico'),
        ('SMS', 'SMS'),
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


