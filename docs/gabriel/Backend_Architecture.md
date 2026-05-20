# Arquitectura Backend y Flujo de Autenticación

**Responsables:** Cristian Velasco y Gabriel Paz  
**Proyecto:** GestionAPP  

---

## 1. Diseño de Autenticación (REQ-01)
Se ha implementado un flujo de autenticación profesional utilizando las herramientas nativas de Django, pero personalizadas para los roles de la clínica:
*   **Vistas:** Uso de `LoginView` con templates personalizados.
*   **Mensajes:** Feedback dinámico mediante `django.contrib.messages` para errores de credenciales (Usuario/Password incorrectos).
*   **Seguridad:** Middleware para protección de rutas y `LoginRequiredMixin` en vistas críticas.

---

## 2. API REST y Tokens (Sprint 2)
Para la integración con sistemas externos y el futuro desarrollo móvil, se ha configurado **Django REST Framework**:
*   **Tokens:** Implementación de `TokenAuthentication`.
*   **Serializers:** Validación de datos en la entrada de la API para mantener la integridad (REQ-16).

---

## 3. Lógica de Servicios (Service Layer)
Siguiendo los principios de "Clean Code", la lógica de negocio se ha extraído de las vistas hacia:
*   `availability_service.py`: Encargado de la validación de traslapes y reglas de negocio complejas.
*   **Beneficio:** Facilita las pruebas unitarias automatizadas y la reutilización de código en diferentes interfaces (Web y API).

---

## 4. Managers Personalizados (Custom Managers)
Se han implementado `DisponibilidadManager` y `CitaMedicaManager` para encapsular consultas de base de datos reutilizables:
*   **Encapsulamiento:** Las vistas ya no conocen los detalles del filtrado (ej. `fecha__gte=now().date()`), solo invocan métodos semánticos como `activas_paciente()`.
*   **Mantenibilidad:** Cambios en las reglas de consulta se realizan en un solo lugar (el modelo), impactando tanto a la Web como a la API.

---

## 5. Evidencia de Índices y Optimización
*   **Índices:** Aplicados mediante `Meta.indexes` en los modelos críticos.
*   **Rendimiento:** Reducción de latencia en consultas de agenda masivas.

---
*Manual de Arquitectura para Desarrolladores - Sprint 2.*
