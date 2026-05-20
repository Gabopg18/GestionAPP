from django.core.exceptions import ValidationError
from django.db import transaction
from datetime import datetime
from ..models import disponibilidad, CitaMedica

class AvailabilityService:
    @staticmethod
    def validate_and_create(medico, fecha, hora_inicio, hora_fin):
        """
        Lógica centralizada para validar y crear una disponibilidad.
        Garantiza que no haya traslapes ni citas programadas en el rango.
        """
        # 1. Validar que la hora de inicio sea menor a la de fin
        if hora_inicio >= hora_fin:
            raise ValidationError("La hora de inicio debe ser anterior a la hora de fin.")

        with transaction.atomic():
            # 2. Buscar traslapes (Mismo médico, misma fecha)
            # Un traslape ocurre si (Inicio < d.Fin) Y (Fin > d.Inicio)
            overlaps = disponibilidad.objects.filter(
                medico=medico,
                fecha=fecha,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio
            )

            if overlaps.exists():
                raise ValidationError(
                    f"Conflicto de horario: Ya existe una disponibilidad registrada en este rango ({hora_inicio} - {hora_fin})."
                )

            # 3. Verificar que no existan citas agendadas que queden "huérfanas"
            start_dt = datetime.combine(fecha, hora_inicio)
            end_dt = datetime.combine(fecha, hora_fin)
            
            citas_conflictivas = CitaMedica.objects.filter(
                medico=medico,
                fecha_hora_cita__gte=start_dt,
                fecha_hora_cita__lt=end_dt,
                estado__in=['Pendiente', 'Confirmada']
            )

            if citas_conflictivas.exists():
                raise ValidationError(
                    "No se puede crear/modificar la disponibilidad: Existen citas programadas en este rango."
                )

            # 4. Creación del registro
            return disponibilidad.objects.create(
                medico=medico,
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin
            )

    @staticmethod
    def delete_safe(disponibilidad_obj):
        """
        Elimina una disponibilidad solo si no tiene citas asociadas.
        """
        start_dt = datetime.combine(disponibilidad_obj.fecha, disponibilidad_obj.hora_inicio)
        end_dt = datetime.combine(disponibilidad_obj.fecha, disponibilidad_obj.hora_fin)
        
        citas = CitaMedica.objects.filter(
            medico=disponibilidad_obj.medico,
            fecha_hora_cita__gte=start_dt,
            fecha_hora_cita__lt=end_dt,
            estado__in=['Pendiente', 'Confirmada']
        )

        if citas.exists():
            raise ValidationError("No se puede eliminar: Esta disponibilidad tiene citas programadas.")
        
        disponibilidad_obj.delete()
 
    @staticmethod
    def book_appointment(paciente, disponibilidad_obj, notas=""):
        """
        Agenda una cita y elimina la disponibilidad de forma atómica.
        (REQ-19: Transaccionalidad)
        """
        with transaction.atomic():
            # Crear la cita usando la fecha de la disponibilidad
            fecha_cita = datetime.combine(disponibilidad_obj.fecha, disponibilidad_obj.hora_inicio)
            
            cita = CitaMedica.objects.create(
                paciente=paciente,
                medico=disponibilidad_obj.medico,
                fecha_hora_cita=fecha_cita,
                notas_paciente=notas,
                estado='Pendiente'
            )
            
            # Al agendar, la disponibilidad ya no existe (se convierte en cita)
            disponibilidad_obj.delete()
            
            return cita
