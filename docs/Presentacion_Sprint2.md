# Guion y Estructura de la Presentación (Sprint Review 2)

Este documento contiene el contenido exacto que deben poner en cada diapositiva de su PowerPoint.

---

## Diapositiva 1: Portada
- **Título:** Proyecto GestionAPP - Sprint 2
- **Subtítulo:** Sistema Integral de Citas Médicas y Disponibilidad
- **Integrantes:** Carlo Benavides, Danilo Lara, Gabriel Paz, Juan Sebastián Mayorga.

---

## Diapositiva 2: Objetivo del Sprint 2 y Demostración
- **Título:** Historias de Usuario Implementadas y Demo
- **Contenido:**
  - Desarrollo de API REST para futura integración.
  - Generación de reportes PDF y Dashboard de administración.
  - Validación de traslapes en agendas médicas.
  - **[ESPACIO PARA DEMOSTRACIÓN EN VIVO DEL SOFTWARE]** (Muestren cómo un paciente agenda, y cómo el médico ve su calendario).

---

## Diapositiva 3: Stack Tecnológico
- **Título:** Arquitectura y Tecnologías
- **Backend:** Python con framework Django. Lógica dividida en vistas y capa de servicios (Clean Code).
- **Frontend:** HTML5, CSS3, JavaScript. Integración de FullCalendar para gestión visual de agendas.
- **API:** Django REST Framework (DRF) con autenticación basada en tokens.
- **Base de Datos:** SQLite (Entorno de Desarrollo) con estructura preparada para migración a PostgreSQL.

---

## Diapositiva 4: Carlo Benavides (Requerimientos y Lógica)
- **Título:** Requerimientos Funcionales y Lógica de Negocio
- **Responsabilidad:** 
  - Levantamiento y estructuración de Requerimientos (REQ-01 a REQ-11).
  - Criterios de Aceptación (Given-When-Then).
  - Algoritmo lógico para cálculo de traslapes y espacios libres de la agenda médica.

---

## Diapositiva 5: Danilo Lara (Scrum Master)
- **Título:** Gestión Ágil y Seguimiento
- **Responsabilidad:** 
  - Mantenimiento y priorización del Backlog en Jira.
  - Planificación del Sprint 2 (Definition of Ready).
  - Gestión de Riesgos y seguimiento de minutas de Daily Scrum.

---

## Diapositiva 6: Gabriel Paz (Arquitectura Backend)
- **Título:** Arquitectura y Seguridad Base
- **Responsabilidad:** 
  - Diseño del flujo de autenticación y autorización (Login Required).
  - Creación de la capa de Servicios y Custom Managers para optimizar consultas de BD.
  - Diseño de la API REST e implementación de Serializadores.

---

## Diapositiva 7: Juan Sebastián Mayorga (Ingeniería de Calidad)
- **Título:** Calidad de Software (QA)
- **Responsabilidad:** 
  - Auditoría general basada en los 10 atributos de la norma ISO/IEC 25010.
  - Pruebas de rendimiento (Locust) alcanzando P95 < 2 segundos.
  - Pruebas Unitarias de modelos y seguridad (ocultamiento de credenciales en `.env`).

---

## Diapositiva 8: Backlog de Jira
- **Título:** Estado del Backlog (Sprint 2)
- **Contenido:**
  - *Pegar aquí un screenshot (captura de pantalla) del tablero de Jira mostrando todas las tareas en la columna "Terminado / Done".*

---

## Diapositiva 9: Retrospectiva
- **Título:** Retrospectiva del Curso y Proyecto
- **Lo que estuvo bien:** 
  - Excelente comunicación del equipo usando metodologías ágiles.
  - Aprendizaje profundo de arquitecturas escalables y estándares de calidad (ISO 25010).
- **Lo que hay para mejorar:** 
  - Inicialmente subestimamos la complejidad del manejo de fechas y traslapes en el calendario.
- **Sugerencias para el curso:** 
  - Incluir talleres más profundos de automatización de pruebas (CI/CD) desde el primer sprint.

---

*(Fin de la presentación. Recuerden practicar el tiempo para no pasarse de los 15 minutos)*
