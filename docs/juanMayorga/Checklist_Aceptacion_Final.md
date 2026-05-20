# Checklist de Aceptación Consolidado (Entrega Final)

**Rol Responsable:** Ingeniería de Calidad (Juan Mayorga) en coordinación con Requerimientos (Carlo Benavides).  
**Proyecto:** GestionAPP (Sprint 2)

A continuación se unifican los criterios de aceptación generales exigidos para la entrega final con las reglas de negocio específicas de GestionAPP. Este checklist garantiza que el sistema está listo para pasar a producción.

| ID | Criterio de Aceptación (Adaptado a GestionAPP) | ¿Cumple? (Sí/No) | Observaciones |
|:---|:---|:---|:---|
| **1** | El sistema Backend (Django) se despliega o ejecuta correctamente en el entorno de desarrollo/pruebas sin errores críticos que impidan su inicio. | Sí | El servidor inicia correctamente con `python manage.py runserver` y la DB migra sin fallos. |
| **2** | El proyecto carga en un tiempo aceptable y cumple el RNF de rendimiento (< 2 segundos en P95). | Sí | Validado mediante las pruebas de estrés con Locust detalladas en el reporte de rendimiento. |
| **3** | Los endpoints REST devuelven los datos correctos en JSON y la lógica del modelo bloquea traslapes de horarios (GES-14). | Sí | Validado con éxito. Se intentó registrar una disponibilidad cruzada en Postman y el sistema devolvió un `400 Bad Request` validando la unicidad. |
| **4** | La navegación y el uso del calendario interactivo (FullCalendar) es fluida en escritorio y dispositivos móviles (GES-32). | Sí | El calendario se adapta de forma responsiva y carga vía AJAX en menos de 2s (GES-15). |
| **5** | No se presentan errores visibles en la consola de Django ni en la consola del navegador del usuario. | Sí | Monitoreado durante la auditoría de calidad. |
| **6** | Las pruebas unitarias (Django `TestCase`) pasan correctamente, incluyendo la prueba de validación de traslapes (GES-31). | Sí | El 100% de los tests unitarios (`TST-01`) definidos pasan correctamente. |
| **7** | Las pruebas de integración de la API con Postman se ejecutan exitosamente (códigos 200 GET, 201 POST). | Sí | Se cuenta con la colección JSON de Postman y capturas de pantalla de la creación de disponibilidades. |
| **8** | Se cumplen los protocolos de seguridad básicos: La `SECRET_KEY` y credenciales de BD están ocultas mediante `.env` (GES-33). | Sí | Validado en la auditoría técnica (ISO 25010). El proyecto hace uso de `python-dotenv`. |
| **9** | Los estados de las citas (Pendiente, Confirmada, etc.) se gestionan correctamente y registran la fecha de modificación (GES-16). | Sí | Confirmado en el panel administrativo de Django. |

---
**Firma de Aprobación de QA:** Juan Sebastián Mayorga  
**Fecha de Validación:** 2026-05-20  
*Resultado Final: **Aprobado para Producción**.*
