# Plan Maestro de Pruebas (Master Test Plan)

**Responsable:** Juan Sebastián Mayorga (Ingeniero de Calidad)  
**Sprint:** 2

---

## 1. Casos de Prueba Unitarios (Unit Tests)

| ID | Caso de Prueba | Descripción | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **UT-01** | **Traslapes Críticos** | Intentar crear dos disponibilidades que se solapen en la misma especialidad. | `ValidationError` lanzado por el modelo/servicio. |
| **UT-02** | **Integridad de Agenda** | Registrar una disponibilidad sobre una cita ya existente. | Bloqueo de la operación para proteger la cita. |
| **UT-03** | **API FullCalendar** | Consultar el endpoint `/api/disponibilidades/`. | Respuesta JSON con formato de eventos (título, inicio, fin). |

---

## 2. Pruebas de Integración

*   **Flujo Completo:** Validación del proceso desde que el médico registra su horario hasta que el paciente lo visualiza en el portal de citas.
*   **Seguridad:** Verificación de que un usuario no autenticado reciba un `403 Forbidden` al intentar acceder a la API de médicos.

---

## 3. Pruebas de Interfaz (UI Tests)

*   **FullCalendar Interactivo:** Comprobar que los bloques de disponibilidad cambian de color según su estado (Verde = Libre, Rojo = Ocupado).
*   **Responsive Design:** Validar que el calendario sea usable en pantallas de smartphones.

---

## 4. Pruebas de Performance (Locust)
*   Simulación de 50 usuarios concurrentes.
*   Métrica clave: Tiempo de respuesta P95 < 2s (RNF-01).

---
*Plan de Calidad aprobado para el Sprint 2.*
