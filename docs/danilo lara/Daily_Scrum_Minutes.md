# 📅 Minutas de Daily Scrum - Sprint 2

**Scrum Master:** Danilo Lara  
**Proyecto:** GestionAPP  

---

## Daily Scrum - Día 1
*   **Avances:** Carlos entregó los nuevos criterios de aceptación (AC) para el Dashboard. Cristian inició la configuración de DRF.
*   **Bloqueos:** Juan reporta que el linter del IDE no reconoce los módulos de Django (Falso positivo). Se procede sin impacto.
*   **Decisiones:** Priorizar el servicio de disponibilidad antes que la API.

## Daily Scrum - Día 2
*   **Avances:** Gabriel terminó los índices en los modelos. El rendimiento en consultas locales mejoró un 15%.
*   **Bloqueos:** Problemas de sintaxis en el JS del Dashboard (Arreglado hoy).
*   **Decisiones:** Implementar `xhtml2pdf` en lugar de ReportLab por su facilidad con plantillas HTML.

## Daily Scrum - Día 3 (Cierre)
*   **Avances:** Notificaciones por correo HTML integradas. Suite de documentación completada.
*   **Bloqueos:** Ninguno.
*   **Decisiones:** Preparar el entorno para la auditoría final de ISO 25010.

---

## 🛑 Registro de Bloqueos Resueltos (Impediments Log)
1.  **Librería PDF:** Se evaluó `xhtml2pdf` vs `ReportLab`. Decisión: `xhtml2pdf` por ahorro de tiempo en diseño.
2.  **Sintaxis Chart.js:** Error de renderizado en el Dashboard resuelto mediante el uso de filtros `{% if not forloop.last %}`.
3.  **Ambiente:** Se creó el archivo `requirements.txt` para asegurar que todo el equipo trabaje con las mismas versiones.

---
*Documento de gestión ágil - GestionAPP.*
