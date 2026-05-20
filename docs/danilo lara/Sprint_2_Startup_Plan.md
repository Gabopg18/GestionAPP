# Plan de Inicio - Sprint 2

**Scrum Master:** Danilo Lara  
**Proyecto:** GestionAPP  
**Período:** [Fecha Inicio] - [Fecha Fin]

---

## 1. Objetivos del Sprint 2
El enfoque de este sprint es la **Exponencialidad y Reportabilidad**. Pasaremos de un sistema de gestión interna a uno con capacidades de API e inteligencia de datos.

*   **Meta 1:** Desplegar la API REST para integración futura con móviles.
*   **Meta 2:** Implementar el módulo de descarga de PDF para pacientes.
*   **Meta 3:** Entregar el Dashboard Analítico para la gerencia.

---

## 2. Definición de "Listo" (Definition of Ready - DoR)
Para iniciar las tareas de este sprint, se requiere:
- [x] Requerimientos técnicos (RQ-16 a RQ-20) definidos por Carlos.
- [x] Librerías (DRF, xhtml2pdf) instaladas en el entorno de desarrollo.
- [x] Estructura de servicios (`services/`) diseñada.

---

## 3. Cronograma Sugerido de Dailies
*   **Semana 1:** Enfoque en la arquitectura de la API (Serializers y Viewsets).
*   **Semana 2:** Desarrollo de la lógica de PDF y Dashboard Visual.
*   **Cierre:** Pruebas de integración de la API y auditoría de carga (Locust).

---

## 4. Gestión de Riesgos Identificados
| Riesgo | Impacto | Plan de Mitigación |
| :--- | :--- | :--- |
| Complejidad en el diseño de los Serializers. | Alto | Cristian y Gabriel iniciarán con la documentación de DRF desde el día 1. |
| Problemas de formato en la generación del PDF. | Medio | Se utilizarán plantillas HTML simples y Bootstrap embebido. |

---
*Documento de planificación inicial - Sprint 2.*
