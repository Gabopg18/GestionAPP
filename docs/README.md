# Guía de Estudio y Resumen Final - Sprint 2 (100% Completado)

¡Equipo! Este documento es el resumen general de toda la documentación generada durante el **Sprint 2** del proyecto **GestionAPP**. Todos los objetivos planteados, historias de usuario y requerimientos de calidad han sido alcanzados al **100%**. 

Esta guía está diseñada para que todos puedan estudiar y repasar el trabajo de cada integrante antes de la **Sprint Review y la Retrospectiva**.

---

## Estado General del Proyecto
* **Progreso del Sprint 2:** 100% Completado (Aprobado)
* **Pruebas y QA:** 100% Aprobado
* **Documentación:** 100% Finalizada

---

## Resumen por Integrante (Para la Presentación)

A continuación, se detalla exhaustivamente la contribución y responsabilidad de cada miembro del equipo. **Asegúrense de leer la sección de sus compañeros** para entender el proyecto de forma holística.

### 1. Carlo Benavides (Requerimientos y Lógica de Negocio)
**Carpeta:** `docs/carloBenavides/`

Carlo fue el encargado de definir *qué* debe hacer el sistema y asegurar que la lógica base estuviera sólida.
* **Definición de Requerimientos:** Documentó los requerimientos funcionales (REQ-01 al REQ-11) y no funcionales (RNF-01 al RNF-08) asegurando que el software cumpla con lo esperado por el cliente.
* **Backlog de Jira (`Backlog_Requerimientos_Jira.md`):** Mantuvo el backlog ordenado y priorizado, lo cual es vital para demostrar en la presentación el avance de las historias de usuario.
* **Criterios de Aceptación (`Acceptance_Criteria_Detailed.md`):** Escribió las condiciones exactas (formato *Given-When-Then*) que debían cumplirse para dar una historia de usuario por terminada (ej. Iniciar sesión, agendar cita, cancelar).
* **Lógica de Agenda (`agenda_logic.md`):** Estructuró cómo el sistema debía calcular los espacios libres y ocupados para evitar problemas operativos en la clínica.

### 2. Danilo Lara (Scrum Master y Gestión Ágil)
**Carpeta:** `docs/danilo lara/`

Danilo lideró la metodología ágil, garantizando que el equipo no se desviara y entregara valor al 100%.
* **Plan de Inicio Sprint 2 (`Sprint_2_Startup_Plan.md`):** Definió las metas claras del sprint (Exponencialidad, API REST, PDFs, Dashboards). Implementó la "Definition of Ready (DoR)" para asegurar que las tareas se pudieran iniciar sin bloqueos.
* **Minutas de Daily Scrum (`Daily_Scrum_Minutes.md`):** Llevó el registro diario de qué hizo cada uno, qué iba a hacer y qué bloqueos tenían, manteniendo el flujo de trabajo continuo.
* **Gestión de Riesgos:** Identificó preventivamente riesgos (como la complejidad de serializadores y problemas con PDFs) y estableció planes de mitigación tempranos.
* **Reporte de Gestión (`Sprint_1_Management_Report.md`):** Consolidó las métricas de gestión del equipo para la mejora continua.

### 3. Gabriel Paz (Arquitectura Backend y Base de Datos)
**Carpeta:** `docs/gabriel/`

Gabriel (junto con el equipo de desarrollo) diseñó el motor y la estructura interna del sistema usando Django.
* **Arquitectura Backend (`Backend_Architecture.md`):** 
  * Implementó un sistema de **Autenticación Seguro** y protegido.
  * Diseñó la **API REST** usando *Django REST Framework (DRF)* con *Tokens Authentication*, dejando el sistema listo para integrarse con apps móviles.
  * Separó la lógica de negocio usando **Servicios** (Clean Code) creando `availability_service.py` para no sobrecargar las vistas.
  * Creó **Custom Managers** (`DisponibilidadManager`) para optimizar las consultas a la base de datos de manera centralizada.
* **Plan de Migración PostgreSQL (`PostgreSQL_Migration_Plan.md`):** Preparó la estrategia técnica para mover la base de datos de SQLite a un entorno de producción robusto con PostgreSQL, asegurando la escalabilidad del sistema.

### 4. Juan Sebastián Mayorga (Ingeniería de Calidad - QA)
**Carpeta:** `docs/juanMayorga/`

Juan aseguró que el código construido fuera robusto, seguro, rápido y cumpliera estándares internacionales.
* **Auditoría ISO 25010 (`ISO25010_Security_Audit.md`):** Lideró la auditoría asegurando que el sistema es seguro (ocultando credenciales), fiable y mantenible. *(Nota: La evaluación exhaustiva de los 10 atributos para la entrega final se encuentra en `Evaluacion_ISO25010_Sprint2.md`)*.
* **Plan Maestro de Pruebas (`Master_Test_Plan.md`):** Definió los Casos de Prueba Unitarios (UT), Pruebas de Integración y Pruebas de Interfaz (UI) comprobando que funcionalidades críticas como los traslapes de agenda no fallaran.
* **Rendimiento con Locust (`Locust_Performance_Report.md`):** Ejecutó pruebas de estrés simulando múltiples usuarios concurrentes para garantizar que el P95 del tiempo de respuesta fuera menor a 2 segundos.
* **Seguridad y Variables (`Environment_Variables_Checklist.md`):** Implementó la protección del entorno configurando variables ocultas en `.env`, mitigando fugas de credenciales.

---

## Puntos Clave para Estudiar para la Presentación

1. **El Stack Tecnológico:** 
   * **Backend:** Python + Django.
   * **API:** Django REST Framework (DRF).
   * **Frontend:** HTML, CSS (Bootstrap), JavaScript (AJAX para FullCalendar).
   * **Base de Datos:** SQLite (Entorno de desarrollo) listo para migrar a PostgreSQL (Producción).
2. **El Logro Principal del Sprint 2:** Convertimos un sistema de gestión web básico en una plataforma escalable con una API REST y aseguramos su calidad mediante métricas (Rendimiento < 2s, 0 traslapes de citas permitidos).
3. **Calidad de Software:** Todo el sistema se testeó y evaluó siguiendo la norma internacional **ISO/IEC 25010**, garantizando no solo que funcione (funcional), sino que sea seguro, eficiente y mantenible (no funcional).

> **Mensaje Final:** ¡El proyecto está excelente y completo! Repasen sus respectivas secciones para que cada uno pueda explicar con seguridad su área de responsabilidad en la Sprint Review. ¡Éxitos en la presentación!
