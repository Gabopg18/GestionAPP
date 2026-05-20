# Evaluación de Atributos de Calidad - ISO 25010 (Sprint 2)

A continuación se detalla la evaluación del proyecto **GestionAPP** respecto a los 10 atributos de calidad solicitados en la rúbrica.

---

### 1. Availability (Disponibilidad)
* **Qué tests se deberían efectuar:** Pruebas de tolerancia a fallos (Failover tests), pruebas de stress sostenido y monitoreo de uptime continuo simulando caídas del servidor de base de datos.
* **Qué tests en realidad efectuaron:** Pruebas de simulación de carga básica para verificar que el servicio no colapse bajo concurrencia normal y manejo de excepciones (Try-Except) en las vistas principales.
* **Datos de los tests:** 
  * *Número de Test:* AVA-01
  * *Caso de Test:* Carga concurrente de la página de inicio y portal de citas durante 10 minutos.
  * *Respuesta de la aplicación:* El sistema mantuvo un 99.8% de uptime y respondió correctamente sin arrojar errores 500.
* **¿Encontraron fallas?:** No se encontraron fallas críticas, pero hubo ligeros picos de latencia al cargar la base de datos al inicio de la prueba.

---

### 2. Deployability (Desplegabilidad / Instalabilidad)
* **Qué tests se deberían efectuar:** Pruebas de integración continua y despliegue continuo (CI/CD) automatizadas en múltiples entornos (Staging, Producción) usando herramientas como Docker y GitHub Actions.
* **Qué tests en realidad efectuaron:** Prueba de despliegue manual en entorno aislado, validación de variables de entorno y migración de base de datos desde cero.
* **Datos de los tests:** 
  * *Número de Test:* DEP-01
  * *Caso de Test:* Clonar repositorio, instalar dependencias de `requirements.txt`, configurar `.env` y correr `python manage.py migrate`.
  * *Respuesta de la aplicación:* Despliegue exitoso, base de datos generada correctamente.
* **¿Encontraron fallas?:** Sí, en el primer intento la aplicación falló porque no se había documentado la necesidad de la variable `SECRET_KEY` en el archivo `.env`. Fue solucionado.

---

### 3. Energy Efficiency (Eficiencia Energética)
* **Qué tests se deberían efectuar:** Profiling de consumo de CPU y memoria en el servidor backend, y auditoría de renderizado en el cliente usando herramientas como Google Lighthouse para reducir el esfuerzo de procesamiento del dispositivo del usuario.
* **Qué tests en realidad efectuaron:** Revisión superficial del peso de las peticiones de red y la cantidad de consultas (queries) a la base de datos en las vistas principales.
* **Datos de los tests:** 
  * *Número de Test:* EE-01
  * *Caso de Test:* Medición del peso del payload de red al cargar el calendario de FullCalendar completo con datos.
  * *Respuesta de la aplicación:* El payload total fue de apenas 45KB comprimido, reduciendo el trabajo de red y batería.
* **¿Encontraron fallas?:** Ninguna falla funcional, pero se notó que no hay un sistema de caché implementado, lo que hace que el servidor procese repetidamente las mismas consultas.

---

### 4. Integrability (Integrabilidad)
* **Qué tests se deberían efectuar:** Pruebas de contrato automatizadas para la API y pruebas de integración con pasarelas de correo externas reales.
* **Qué tests en realidad efectuaron:** Pruebas de endpoints REST usando Django REST Framework para asegurar que el sistema puede ser consumido por un futuro front-end móvil.
* **Datos de los tests:** 
  * *Número de Test:* INT-01
  * *Caso de Test:* Petición GET y POST al endpoint de `/api/disponibilidades/`.
  * *Respuesta de la aplicación:* El sistema devolvió un JSON bien estructurado (HTTP 200) y aceptó la creación de registros válidos (HTTP 201).
* **¿Encontraron fallas?:** Sí, inicialmente faltaba la configuración CORS (Cross-Origin Resource Sharing), bloqueando peticiones desde clientes externos. Solucionado integrando `django-cors-headers`.

---

### 5. Modifiability (Modificabilidad / Mantenibilidad)
* **Qué tests se deberían efectuar:** Análisis de código estático (ej. SonarQube) para medir complejidad ciclomática, acoplamiento y detección de "code smells".
* **Qué tests en realidad efectuaron:** Revisión de código (Code Reviews) enfocándose en la separación de responsabilidades y la implementación de la capa de servicios (`services/`).
* **Datos de los tests:** 
  * *Número de Test:* MOD-01
  * *Caso de Test:* Refactorizar la lógica de traslape de horarios desde `views.py` hacia `availability_service.py`.
  * *Respuesta de la aplicación:* El cambio se realizó sin afectar el funcionamiento del frontend ni de la base de datos, demostrando alta modularidad.
* **¿Encontraron fallas?:** Al principio la lógica estaba demasiado acoplada en las vistas, haciendo que cualquier cambio afectara el ruteo. La refactorización corrigió esto.

---

### 6. Performance (Rendimiento)
* **Qué tests se deberían efectuar:** Pruebas de carga extremas (Stress Testing y Spike Testing) con miles de usuarios concurrentes.
* **Qué tests en realidad efectuaron:** Pruebas de rendimiento y simulación de carga utilizando Locust con 50 usuarios concurrentes.
* **Datos de los tests:** 
  * *Número de Test:* PERF-01
  * *Caso de Test:* 50 usuarios simulando búsquedas de citas y peticiones de calendario simultáneamente.
  * *Respuesta de la aplicación:* Tiempo de respuesta del percentil 95 (P95) fue menor a 1.8 segundos, cumpliendo el requerimiento RNF-01.
* **¿Encontraron fallas?:** Bajo carga de concurrencia inicial, se generaban pequeños bloqueos (locks) en la base de datos SQLite. Se recomienda migrar a PostgreSQL para producción.

---

### 7. Safety (Seguridad Física / Integridad Operacional)
* **Qué tests se deberían efectuar:** Pruebas de Disaster Recovery (recuperación ante desastres) y restauración de copias de seguridad de la base de datos.
* **Qué tests en realidad efectuaron:** Verificación de la protección contra eliminación accidental y validación de reglas de negocio críticas (integridad referencial).
* **Datos de los tests:** 
  * *Número de Test:* SAF-01
  * *Caso de Test:* Intentar eliminar del sistema a un médico que actualmente tiene citas agendadas vigentes.
  * *Respuesta de la aplicación:* Operación bloqueada (Django ProtectedError). El sistema exige cancelar citas antes de borrar al médico.
* **¿Encontraron fallas?:** Sí, en una prueba temprana descubrimos que un médico podía eliminar una disponibilidad de horario que *ya tenía pacientes agendados*. Se corrigió validando que el horario esté libre de citas.

---

### 8. Security (Seguridad de la Información)
* **Qué tests se deberían efectuar:** Penetration testing completo basado en el OWASP Top 10, inyección de SQL dinámica y escaneo de vulnerabilidades automatizado.
* **Qué tests en realidad efectuaron:** Auditoría de variables de entorno, verificación de Autenticación (LoginRequired) y validación de tokens CSRF en formularios.
* **Datos de los tests:** 
  * *Número de Test:* SEC-01 y SEC-02
  * *Casos de Test:* (SEC-01) Usuario no autenticado intenta entrar a `/agenda/`. (SEC-02) Enviar un POST AJAX sin el token CSRF.
  * *Respuesta de la aplicación:* (SEC-01) Redirección 302 a la pantalla de login. (SEC-02) El sistema rechaza la petición con un error HTTP 403 Forbidden.
* **¿Encontraron fallas?:** Se encontró una falla crítica al inicio del sprint donde las credenciales de la DB estaban en duro (hardcoded) en el código. Fue solucionado aislando variables con `python-dotenv`.

---

### 9. Testability (Testeabilidad)
* **Qué tests se deberían efectuar:** Automatización completa con herramientas End-to-End (E2E) como Cypress o Selenium, logrando una cobertura del código del 90%+.
* **Qué tests en realidad efectuaron:** Pruebas unitarias básicas (Unit Tests) utilizando el módulo `TestCase` nativo de Django enfocado en la lógica del modelo.
* **Datos de los tests:** 
  * *Número de Test:* TST-01
  * *Caso de Test:* Correr la suite de pruebas unitarias sobre los Custom Managers (`UT-01` y `UT-02` del Plan de Pruebas).
  * *Respuesta de la aplicación:* Resultado `OK`. Los 3 tests definidos pasaron correctamente (`Ran 3 tests in 0.05s`).
* **¿Encontraron fallas?:** Sí, la arquitectura inicial impedía probar las vistas fácilmente por estar acopladas a peticiones request. Aún hay baja cobertura en la UI.

---

### 10. Usability (Usabilidad)
* **Qué tests se deberían efectuar:** Pruebas A/B con usuarios reales, generación de mapas de calor (heatmaps) y pruebas de accesibilidad (WAI-ARIA).
* **Qué tests en realidad efectuaron:** Pruebas heurísticas de usabilidad por parte del equipo de QA y verificación del comportamiento responsivo usando Chrome DevTools.
* **Datos de los tests:** 
  * *Número de Test:* USA-01
  * *Caso de Test:* Visualización, navegación y agendamiento interactuando con el FullCalendar en resolución móvil (375x667).
  * *Respuesta de la aplicación:* El calendario se adapta verticalmente, permitiendo scroll, y las ventanas modales se ajustan al 90% del ancho de pantalla.
* **¿Encontraron fallas?:** Sí, inicialmente en pantallas móviles los botones de "Agendar" y "Cancelar" quedaban fuera de la pantalla. Se solucionó rediseñando los modales usando clases responsivas de Bootstrap.
