from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Medico
import json

class MedicoFiltroTests(TestCase):
    def setUp(self):
        """Configuración inicial para las pruebas"""
        # 1. Crear usuarios base para los médicos
        self.user1 = User.objects.create_user(username='doc_cardiologia', first_name='Juan', last_name='Perez', password='password123')
        self.user2 = User.objects.create_user(username='doc_pediatria', first_name='Ana', last_name='Gomez', password='password123')
        self.user3 = User.objects.create_user(username='doc_cardiologia2', first_name='Carlos', last_name='Ruiz', password='password123')
        
        # 2. Crear los médicos asignándoles los usuarios y sus especialidades
        self.medico1 = Medico.objects.create(user=self.user1, especialidad='Cardiología')
        self.medico2 = Medico.objects.create(user=self.user2, especialidad='Pediatría')
        self.medico3 = Medico.objects.create(user=self.user3, especialidad='Cardiología')
        
        self.client = Client()
        self.url = reverse('obtener_medicos')

    # =========================================================================
    # PRUEBAS DE INTEGRACIÓN
    # =========================================================================

    def test_integracion_filtro_especialidad_exacta(self):
        """
        [Prueba de Integración] 
        Validar que los resultados coincidan exactamente con la especialidad seleccionada (Cardiología).
        """
        response = self.client.get(self.url, {'especialidad': 'Cardiología'})
        
        # 1. Validar respuesta HTTP correcta
        self.assertEqual(response.status_code, 200)
        
        # 2. Parsear el JSON devuelto
        data = json.loads(response.content)
        
        # 3. Verificar que devuelva exactamente los 2 médicos de Cardiología
        self.assertEqual(len(data), 2)
        
        # 4. Validar que CADA registro coincida exactamente con la especialidad
        for medico in data:
            self.assertEqual(medico['especialidad'], 'Cardiología')

    def test_integracion_filtro_otra_especialidad(self):
        """
        [Prueba de Integración]
        Validar la respuesta de la base de datos cuando se solicita 'Pediatría'.
        """
        response = self.client.get(self.url, {'especialidad': 'Pediatría'})
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        
        # Debe haber exactamente 1 médico de Pediatría
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['especialidad'], 'Pediatría')
        self.assertEqual(data[0]['nombre'], 'Ana Gomez')


    # =========================================================================
    # PRUEBAS UNITARIAS DE LA LÓGICA DE FILTRADO
    # =========================================================================

    def test_unitaria_logica_sin_filtros(self):
        """
        [Prueba Unitaria]
        Verifica que la lógica devuelva TODOS los médicos si no se pasa ningún parámetro de filtro.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # Como creamos 3 médicos, deben volver 3
        self.assertEqual(len(data), 3)

    def test_unitaria_logica_especialidad_inexistente(self):
        """
        [Prueba Unitaria]
        Verifica la lógica de filtrado cuando se busca una especialidad que no existe en la BD.
        Debe devolver una lista vacía, no un error.
        """
        response = self.client.get(self.url, {'especialidad': 'Neurología'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # No hay neurólogos en la BD de prueba
        self.assertEqual(len(data), 0)

    def test_unitaria_logica_filtrado_case_insensitive(self):
        """
        [Prueba Unitaria]
        Verifica que la lógica de filtrado ignore mayúsculas y minúsculas (ej: 'cardiología' == 'Cardiología').
        """
        response = self.client.get(self.url, {'especialidad': 'cardiología'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # Debe encontrar a los 2 cardiólogos sin importar las minúsculas
        self.assertEqual(len(data), 2)
        for medico in data:
            self.assertEqual(medico['especialidad'].lower(), 'cardiología')
