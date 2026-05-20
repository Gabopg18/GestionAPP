from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Medico, disponibilidad
from datetime import date, time

class DisponibilidadOverlapTests(TestCase):
    def setUp(self):
        """Configuración de médicos para las pruebas"""
        self.user_pediatra = User.objects.create_user(username='pediatra1', password='password123')
        self.pediatra1 = Medico.objects.create(user=self.user_pediatra, especialidad='Pediatría')
        
        self.user_pediatra2 = User.objects.create_user(username='pediatra2', password='password123')
        self.pediatra2 = Medico.objects.create(user=self.user_pediatra2, especialidad='Pediatría')
        
        self.user_cardiologo = User.objects.create_user(username='cardiologo1', password='password123')
        self.cardiologo1 = Medico.objects.create(user=self.user_cardiologo, especialidad='Cardiología')

        # Horario base: Lunes 9:00 - 10:00 (Pediatra 1)
        self.base_fecha = date(2030, 5, 11)
        self.dispo_base = disponibilidad.objects.create(
            medico=self.pediatra1,
            fecha=self.base_fecha,
            hora_inicio=time(9, 0),
            hora_fin=time(10, 0)
        )

    def test_traslape_total_mismo_medico(self):
        """Caso 1: Un nuevo horario está contenido totalmente en uno existente."""
        nueva_dispo = disponibilidad(
            medico=self.pediatra1,
            fecha=self.base_fecha,
            hora_inicio=time(9, 15),
            hora_fin=time(9, 45)
        )
        with self.assertRaises(ValidationError) as cm:
            nueva_dispo.save()
        self.assertIn("Cruce de horario detectado", str(cm.exception))

    def test_traslape_parcial_inicio(self):
        """Caso 2: El nuevo horario inicia antes y termina durante uno existente."""
        nueva_dispo = disponibilidad(
            medico=self.pediatra1,
            fecha=self.base_fecha,
            hora_inicio=time(8, 30),
            hora_fin=time(9, 30)
        )
        with self.assertRaises(ValidationError):
            nueva_dispo.save()

    def test_traslape_parcial_fin(self):
        """Caso 3: El nuevo horario inicia durante y termina después de uno existente."""
        nueva_dispo = disponibilidad(
            medico=self.pediatra1,
            fecha=self.base_fecha,
            hora_inicio=time(9, 30),
            hora_fin=time(10, 30)
        )
        with self.assertRaises(ValidationError):
            nueva_dispo.save()

    def test_citas_seguidas_permitidas(self):
        """Caso 4: Horarios que terminan justo cuando el otro empieza deben permitirse."""
        # Horario antes: 08:00 - 09:00
        dispo_antes = disponibilidad(
            medico=self.pediatra1,
            fecha=self.base_fecha,
            hora_inicio=time(8, 0),
            hora_fin=time(9, 0)
        )
        dispo_antes.save() # No debe lanzar error

        # Horario después: 10:00 - 11:00
        dispo_despues = disponibilidad(
            medico=self.pediatra1,
            fecha=self.base_fecha,
            hora_inicio=time(10, 0),
            hora_fin=time(11, 0)
        )
        dispo_despues.save() # No debe lanzar error
        
        self.assertEqual(disponibilidad.objects.count(), 3)

    def test_traslape_misma_especialidad_diferente_medico(self):
        """GES-14: Validar que no se crucen horarios de médicos de la misma especialidad."""
        nueva_dispo = disponibilidad(
            medico=self.pediatra2, # Diferente médico, misma especialidad (Pediatría)
            fecha=self.base_fecha,
            hora_inicio=time(9, 30),
            hora_fin=time(10, 30)
        )
        with self.assertRaises(ValidationError) as cm:
            nueva_dispo.save()
        self.assertIn("Cruce de horario detectado", str(cm.exception))
        self.assertIn("especialidad Pediatría", str(cm.exception))

    def test_sin_traslape_diferente_especialidad(self):
        """Diferentes especialidades sí pueden solaparse (si tienen consultorios distintos)."""
        nueva_dispo = disponibilidad(
            medico=self.cardiologo1, # Diferente especialidad (Cardiología)
            fecha=self.base_fecha,
            hora_inicio=time(9, 30),
            hora_fin=time(10, 30)
        )
        nueva_dispo.save() # No debe lanzar error
        self.assertEqual(disponibilidad.objects.count(), 2)

    def test_api_fullcalendar_format(self):
        """GES-32: Verificar que el endpoint devuelva el formato esperado por FullCalendar."""
        from django.urls import reverse
        import json
        
        url = reverse('ajax_disponibilidades')
        response = self.client.get(url, {'medico_id': self.pediatra1.user.id})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # Verificar campos requeridos por FullCalendar
        self.assertTrue(len(data) > 0)
        evento = data[0]
        self.assertIn('title', evento)
        self.assertIn('start', evento)
        self.assertIn('end', evento)
        self.assertIn('color', evento)
        self.assertEqual(evento['title'], 'Disponible')
        self.assertEqual(evento['color'], '#28a745')
