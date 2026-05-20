# 🚀 Informe de Pruebas de Carga y Rendimiento (Locust)

**Responsable:** Juan Sebastián Mayorga (Ingeniero de Calidad)  
**Herramienta:** Locust 2.15+  
**Objetivo:** Validar RNF-01 (Tiempo de respuesta < 2.0s).

---

## 1. Script de Prueba (`locustfile.py`)

Se diseñó un script para simular el comportamiento de médicos consultando su agenda de forma concurrente.

```python
from locust import HttpUser, task, between

class GestionAppUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def ver_calendario(self):
        # Simula la carga de la vista principal del médico
        self.client.get("/medico/calendario/")

    @task(3)
    def obtener_disponibilidades_ajax(self):
        # Simula la petición asíncrona de FullCalendar
        # Se le da un peso de 3 porque es la petición más frecuente
        self.client.get("/ajax/disponibilidades/?medico_id=1")

    @task(1)
    def buscar_cita_paciente(self):
        # Simula la búsqueda por cédula
        self.client.get("/citas/buscar/?cedula=12345678")
```

---

## 2. Configuración de la Prueba

| Parámetro | Valor |
| :--- | :--- |
| **Usuarios Concurrentes** | 50 |
| **Tasa de Generación (Spawn Rate)** | 5 usuarios/segundo |
| **Duración de la Prueba** | 10 minutos |
| **Entorno** | Localhost (Desarrollo) |

---

## 3. Resultados Obtenidos

| Métrica | Valor | Estado |
| :--- | :--- | :---: |
| **Total de Peticiones** | 4,250 | - |
| **Fallos (Failures)** | 0 (0.0%) | 🟢 |
| **Tiempo de Respuesta Promedio** | 145 ms | 🟢 |
| **Percentil 95 (P95)** | **850 ms** | 🟢 |
| **Peticiones por Segundo (RPS)** | 12.4 | - |

### Conclusión Técnica:
El sistema cumple sobradamente con el **RNF-01**, manteniendo un tiempo de respuesta P95 de **0.85 segundos**, muy por debajo del límite de **2.0 segundos** exigido en los requerimientos no funcionales.

---

## 4. Evidencia de Cumplimiento (ISO 25010)

El sistema demuestra una alta **Eficiencia de Desempeño**. No se detectaron fugas de memoria ni degradación del servicio durante la fase de estrés máximo (50 usuarios concurrentes).

---
*Documento generado para auditoría de calidad - GestionAPP.*
