# ✅ Matriz de Criterios de Aceptación (Acceptance Criteria)

**Responsable:** Carlos Benavides (Ingeniero de Requerimientos)  
**Proyecto:** GestionAPP  
**Sprint:** 2

---

| ID Jira | Título | Criterios de Aceptación (AC) |
| :--- | :--- | :--- |
| **GES-14** | Validación de Traslapes | 1. El sistema no debe permitir dos disponibilidades en el mismo rango para la misma especialidad.<br>2. Se permiten horarios contiguos (Ej: 10:00-11:00 y 11:00-12:00). |
| **GES-15** | Calendario FullCalendar | 1. Los eventos deben cargarse vía AJAX en menos de 2s.<br>2. Los bloques deben mostrar colores diferentes para 'Disponible' vs 'Ocupado'. |
| **GES-16** | Estados de Cita | 1. Los estados válidos son: Pendiente, Confirmada, Cancelada, Realizada.<br>2. El cambio de estado debe quedar registrado en `fecha_modificacion`. |
| **GES-31** | Pruebas Unitarias de Lógica | 1. Debe existir un test que valide el bloqueo de traslapes en el modelo.<br>2. El 100% de los tests de disponibilidad deben pasar en verde. |
| **GES-32** | Interfaz Premium | 1. Uso de Bootstrap 5 y iconos de Bootstrap Icons.<br>2. Diseño responsive compatible con móviles. |
| **GES-33** | Auditoría .env | 1. La `SECRET_KEY` no debe estar en `settings.py`.<br>2. El sistema debe cargar variables desde un archivo `.env` externo. |

---
*Este documento asegura la trazabilidad entre el desarrollo y las necesidades del negocio.*
