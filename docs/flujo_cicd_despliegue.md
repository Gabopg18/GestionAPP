# Flujo CI/CD y Configuración de Despliegue en Vercel

Este documento describe la arquitectura y configuración del flujo de Integración y Despliegue Continuo (CI/CD) implementado para el sistema de Gestión de Citas Médicas, así como las adaptaciones necesarias para su alojamiento en Vercel.

## 1. Integración Continua (CI) con GitHub Actions
El proyecto cuenta con un workflow automatizado en GitHub Actions (`.github/workflows/ci-cd.yml`) que se ejecuta con cada `push` o `pull_request` a las ramas principales (`main`, `master`, `develop`). 

El pipeline asegura la calidad del código mediante los siguientes pasos automatizados:
1. **Configuración de Entorno**: Inicia un entorno Linux (Ubuntu) y configura Python 3.10.
2. **Dependencias del Sistema Operativo**: Instala paquetes nativos de Linux (`libcairo2-dev`, `pkg-config`, `python3-dev`). Este paso fue **crucial** para permitir la instalación de `xhtml2pdf` y `pycairo` en la nube, herramientas necesarias para generar los reportes de comprobantes médicos en PDF.
3. **Instalación de Dependencias**: Descarga e instala los módulos de Python listados en `requirements.txt`.
4. **Linting de Código**: Utiliza `flake8` para detectar errores de sintaxis críticos y prevenir que se suba código defectuoso a producción.
5. **Base de Datos y Pruebas Unitarias**: Se preparan las migraciones locales en SQLite y se ejecuta toda la suite de pruebas automatizadas (`python manage.py test`). Si alguna prueba falla, el pipeline se aborta para proteger el servidor.

## 2. Configuración para Vercel (Serverless Hosting)
Para alojar este proyecto Django en la plataforma gratuita de **Vercel**, el proyecto fue estructurado con configuraciones especializadas:

* **Archivos Nativos de Vercel**: 
  * `vercel.json`: Funciona como el "director" del despliegue. Define que el proyecto usa Python y apunta hacia el punto de entrada de Django.
  * `build_files.sh`: Un script pre-despliegue que Vercel ejecuta en la nube para instalar dependencias y recolectar los archivos estáticos (CSS, JS) usando `collectstatic`.
* **Manejo de Estáticos con Whitenoise**: Dado que Vercel no usa servidores tradicionales como Apache o Nginx, se instaló y configuró la librería **WhiteNoise** dentro de los `MIDDLEWARE` de `settings.py` para entregar los recursos visuales correctamente a los usuarios.
* **Adaptación de WSGI**: En `wsgi.py` se incluyó una declaración especial (`app = application`) requerida obligatoriamente por el entorno Serverless de Vercel.
* **Hosts Permitidos**: Se configuró `ALLOWED_HOSTS` para autorizar los dominios dinámicos de `.vercel.app`.

## 3. Estabilización y Buenas Prácticas
Para que el servidor de CI/CD pasara con éxito, se resolvieron varios problemas de la etapa de desarrollo:
* **Limpieza de Dependencias**: Se purgó `requirements.txt`, eliminando elementos como `chart.js` (una librería frontend de JavaScript que no debe ir en el instalador de Python).
* **Fix en Pruebas Unitarias**: Se actualizó la lógica del módulo de pruebas de disponibilidad de médicos, reemplazando fechas quemadas ("hardcodeadas") en el pasado por fechas futuras. Esto evitó que los tests entraran en conflicto con los filtros de tiempo real (`timezone.now()`) de la API.
* **Protección de Variables de Entorno (Seguridad)**: Se implementó un `.gitignore` robusto que excluye carpetas de entorno virtual, cachés y, lo más importante, el archivo `.env`. Las credenciales (claves secretas de Django, contraseñas de correos, etc.) ahora deben configurarse de forma encriptada directamente en el panel *Environment Variables* de Vercel.
