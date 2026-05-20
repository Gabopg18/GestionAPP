# Auditoría de Seguridad e Informe ISO/IEC 25010

**Responsable:** Juan Sebastián Mayorga (Ingeniero de Calidad)  
**Proyecto:** GestionAPP  
**Estado:** Finalizado

---

## 1. Evaluación de Características de Calidad (ISO 25010)

| Característica | Sub-característica | Estado | Evidencia / Acción Tomada |
| :--- | :--- | :---: | :--- |
| **Seguridad** | Confidencialidad | OK | Implementación de `python-dotenv` para ocultar `SECRET_KEY` y credenciales. |
| **Seguridad** | Integridad | OK | Validación de traslapes en el backend para evitar corrupción de la agenda. |
| **Fiabilidad** | Disponibilidad | OK | Diseño orientado a alta disponibilidad y manejo de errores (Try-Except) en vistas. |
| **Eficiencia** | Comportamiento Temporal | OK | Cumplimiento del RNF-01 (< 2s de respuesta) validado con Locust. |
| **Mantenibilidad** | Modularidad | OK | Separación de lógica en `services/` y `views.py` siguiendo arquitectura Django. |

---

## 2. Validación de Seguridad de Variables de Entorno (GES-33)

Se ha realizado una auditoría del archivo `settings.py` y se confirma la mitigación de los siguientes riesgos:

1.  **Exposición de Credenciales:** Se eliminaron las contraseñas de correo y DB del código fuente. Ahora se cargan desde `.env`.
2.  **Modo Debug:** Se configuró `DEBUG=os.getenv('DEBUG')`, asegurando que en producción no se filtren trazas de error al usuario.
3.  **Seguridad de Cookies:** Se recomienda activar `SESSION_COOKIE_SECURE=True` para el despliegue final.

---

## 3. Informe de Resultados de Auditoría

### Hallazgos Críticos:
- **Resuelto:** La lógica de traslapes permitía citas duplicadas. Se implementó el método `clean()` en el modelo para bloquear esto.
- **Resuelto:** No existía protección contra CSRF en las peticiones AJAX del calendario. Se integró `{% csrf_token %}`.

### Recomendaciones:
- Implementar **HTTPS** obligatorio mediante redirección en el servidor (Nginx/Heroku).
- Añadir **Rate Limiting** a la búsqueda de citas para prevenir scraping de datos de pacientes.

---
*Firma: Juan Sebastián Mayorga - QA Lead*
