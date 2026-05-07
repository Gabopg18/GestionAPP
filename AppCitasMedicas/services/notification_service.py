from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

class NotificationService:
    @staticmethod
    def send_appointment_confirmation(cita):
        """Envía un correo HTML de confirmación de cita."""
        if not cita.paciente.correo:
            return False

        subject = f'Confirmación de Cita - GestionAPP - {cita.fecha_hora_cita.strftime("%d/%m/%Y")}'
        from_email = settings.DEFAULT_FROM_EMAIL
        to = cita.paciente.correo

        # Contexto para la plantilla
        context = {
            'cita': cita,
            'paciente_nombre': cita.paciente.nombre,
            'medico_nombre': cita.medico.user.get_full_name(),
            'fecha': cita.fecha_hora_cita.strftime("%d/%m/%Y"),
            'hora': cita.fecha_hora_cita.strftime("%H:%M"),
        }

        # Renderizar HTML y Texto plano
        html_content = render_to_string('AppCitasMedicas/emails/confirmacion_cita.html', context)
        text_content = strip_tags(html_content)

        try:
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return True
        except Exception as e:
            print(f"Error enviando email: {str(e)}")
            return False
