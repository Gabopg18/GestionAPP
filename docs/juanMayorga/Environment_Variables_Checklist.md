# ✅ Checklist de Validación de Variables de Entorno

**Responsable:** Juan Sebastián Mayorga (QA Lead)  
**Proyecto:** GestionAPP  

---

## 1. Variables Críticas (Obligatorias)
| Variable | Descripción | Estado | Prueba de Fallo |
| :--- | :--- | :---: | :--- |
| `SECRET_KEY` | Llave de cifrado de Django. | 🔘 | El servidor debe dar error `KeyError` si falta. |
| `DEBUG` | True para desarrollo, False para prod. | 🔘 | Validar que no se vean trazas en Prod. |
| `DB_NAME` | Nombre de la base de datos Postgres. | 🔘 | Error de conexión al iniciar. |
| `DB_USER` | Usuario de la base de datos. | 🔘 | Error de autenticación. |

## 2. Configuración de Email (Notificaciones REQ-20)
*   [ ] `EMAIL_HOST`: Servidor SMTP (ej. smtp.gmail.com).
*   [ ] `EMAIL_PORT`: 587 (TLS).
*   [ ] `EMAIL_HOST_USER`: Correo emisor.
*   [ ] `EMAIL_HOST_PASSWORD`: Contraseña de aplicación (Secret).

---

## 3. Pruebas de Carga Fallida
Se realizaron pruebas de robustez eliminando temporalmente el archivo `.env`:
*   **Resultado:** El sistema falló de forma controlada indicando la falta de configuración crítica, evitando que la aplicación inicie en un estado inseguro o inestable.

---

## 4. Auditoría de Secretos (Evidencia)
- [x] No hay contraseñas de DB en `settings.py`.
- [x] El archivo `.env` está incluido en `.gitignore`.
- [x] La `SECRET_KEY` de producción es diferente a la de desarrollo.

---
*Validado por el Ingeniero de Calidad.*
