from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import DateInput, TimeInput
from django.utils import timezone
from .models import Paciente, CitaMedica, disponibilidad, Medico 
from datetime import date

class BuscarCitasForm(forms.Form):
    cedula = forms.CharField(
        label='Número de Cédula/ID',
        max_length=20,
        validators=[
            RegexValidator(
                regex='^[0-9]+$',
                message='Solo se permiten números en la cédula'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su cédula'
        })
    )

class CitaMedicaForm(forms.ModelForm):
    fecha_hora_cita = forms.ChoiceField(
        label="Fecha y hora de la cita",
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_fecha_hora_cita',
        }),
        help_text="Primero seleccione un médico para ver disponibilidades"
    )

    class Meta:
        model = CitaMedica
        fields = ['medico', 'fecha_hora_cita']
        widgets = {
            'medico': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_medico',
                'data-ajax-url': '/ajax/disponibilidades/'  # Ajax JS
            })
        }
        labels = {
            'medico': 'Seleccione Médico'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        hoy = timezone.now().date()
        self.fields['medico'].queryset = Medico.objects.filter(
            disponibilidad__fecha__gte=hoy
        ).distinct().order_by('user__last_name')

        self.fields['medico'].empty_label = "-- Seleccione un médico --"

        # Construir dinámicamente las opciones del campo fecha_hora_cita
        data = kwargs.get('data') or self.data
        medico_id = data.get('medico') if data else None

        if medico_id:
            ahora = timezone.now()
            qs = disponibilidad.objects.filter(
                medico_id=medico_id,
                fecha__gte=ahora.date()
            ).exclude(
                fecha=ahora.date(),
                hora_inicio__lt=ahora.time()
            ).order_by('fecha', 'hora_inicio')

            opciones = []
            for d in qs:
                fecha_hora = timezone.datetime.combine(d.fecha, d.hora_inicio)
                fecha_hora_aware = timezone.make_aware(fecha_hora)
                iso = fecha_hora_aware.isoformat()
                mostrar = f"{d.fecha.strftime('%d/%m/%Y')} - {d.hora_inicio.strftime('%H:%M')}"
                opciones.append((iso, mostrar))

            self.fields['fecha_hora_cita'].choices = opciones
        else:
            self.fields['fecha_hora_cita'].choices = [('', '-- Seleccione un médico primero --')]

        # Mensajes de error personalizados
        for field in self.fields.values():
            field.error_messages = {
                'required': f'Por favor seleccione un {field.label.lower()}',
                **field.error_messages
            }



class disponibilidadMedicoForm(forms.ModelForm):
    class Meta:
        model = disponibilidad 
        fields = ['fecha', 'hora_inicio', 'hora_fin']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'class': 'form-control'}),
        }
        labels = {
            'fecha': 'Fecha',
            'hora_inicio': 'Hora de inicio',
            'hora_fin': 'Hora de fin',
        }
    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        
        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise forms.ValidationError(
                'La hora de fin debe ser posterior a la hora de inicio'
            )
        return cleaned_data

class LoginMedicoForm(AuthenticationForm):
    username = forms.CharField(
        label='Nombre de Usuario', # Cambiado a 'Nombre de Usuario'
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su nombre de usuario'
        })
    )
    password = forms.CharField(
        label='contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña'
        })
    )

class ReprogramarCitaForm(forms.ModelForm):
    class Meta:
        model = CitaMedica
        fields = ['fecha_hora_cita']
        widgets = {
            'fecha_hora_cita': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            })
        }
        labels = {
            'fecha_hora_cita': 'Nueva Fecha y Hora',
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_hora = cleaned_data.get('fecha_hora_cita')
        medico = self.instance.medico  # Extraemos el médico asociado a la cita
        cita_id = self.instance.id_cita

        if fecha_hora:
            ahora = timezone.now()
            if fecha_hora < ahora:
                raise forms.ValidationError("No puedes reprogramar citas en horarios pasados.")

            dia_semana = fecha_hora.strftime('%A')
            dias_map = {
                'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
                'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
            }
            dia_semana_es = dias_map.get(dia_semana, '')

            hora = fecha_hora.time()

            disponible = disponibilidad.objects.filter(
                medico=medico,
                fecha=fecha_hora.date(),
                hora_inicio__lte=hora,
                hora_fin__gte=hora
            ).exists()

            if not disponible:
                raise forms.ValidationError(f"El Dr./Dra. {medico.user.username} no tiene disponibilidad registrada para ese horario.")

            cita_existente = CitaMedica.objects.filter(
                medico=medico,
                fecha_hora_cita=fecha_hora,
                estado__in=['Agendada', 'Reprogramada']
            ).exclude(id_cita=cita_id).exists()

            if cita_existente:
                raise forms.ValidationError("Ya existe otra cita en ese horario con el mismo médico.")

        return cleaned_data
    
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['cedula', 'nombre', 'telefono', 'direccion', 'correo', 'fecha_nacimiento']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }



