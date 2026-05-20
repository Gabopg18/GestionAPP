# 📋 Backlog de Requerimientos Técnicos - Sprint 2

Este documento detalla los requerimientos (RQ) para el **Sprint 2**, enfocados en la expansión del sistema y modernización de la arquitectura.

---

## 🔝 Product Backlog del Sprint 2

| ID RQ | Título del Requerimiento | Prioridad | Estimación (Puntos) | Criterio de Validación |
| :--- | :--- | :---: | :---: | :--- |
| **REQ-16** | Implementación de API REST (DRF) | ⭐ Crítica | 8 | Endpoints JSON funcionales |
| **REQ-17** | Generación de Reportes PDF de Citas | ⬆️ Alta | 5 | Descarga de documento válido |
| **REQ-18** | Dashboard de Analítica (Admin) | ⬆️ Alta | 8 | Gráficos y estadísticas visibles |
| **REQ-19** | Refactorización a Services/Managers | ➡️ Media | 5 | Código desacoplado y testeado |
| **REQ-20** | Notificaciones Push/Email Mejoradas | ➡️ Media | 3 | Envío de plantillas HTML |

---

## 🛠️ Especificaciones Técnicas del Sprint 2

### REQ-16: API REST con Django REST Framework
*   **Descripción:** Exponer los modelos de `CitaMedica` y `disponibilidad` mediante una API protegida.
*   **Serializers:** Crear serializers personalizados para manejar la lógica de validación de traslapes en la API.
*   **Seguridad:** Autenticación mediante `TokenAuthentication` o `JWT`.

### REQ-17: Generación de PDF (Reportlab/xhtml2pdf)
*   **Descripción:** El paciente podrá descargar un PDF con la confirmación de su cita.
*   **Contenido:** Logo de la clínica, datos del paciente, médico, fecha, hora y código QR de validación.

---

## 📉 Requerimientos No Funcionales (Sprint 2)

| ID | Nombre | Métrica de Aceptación |
| :--- | :--- | :--- |
| **RNF-09** | Escalabilidad | Soporte para múltiples formatos de salida (JSON, PDF, CSV). |
| **RNF-10** | Usabilidad Visual | Dashboard con componentes de `Chart.js` o `D3.js`. |

---
*Backlog oficial para el inicio del Sprint 2 - GestionAPP.*
