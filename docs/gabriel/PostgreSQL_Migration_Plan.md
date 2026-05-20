# 🐘 Plan de Migración a PostgreSQL

**Responsables:** Cristian Velasco y Gabriel Paz  
**Objetivo:** Migrar la persistencia de datos de SQLite a PostgreSQL para el entorno de producción.

---

## 1. Requisitos Técnicos
*   Librería: `psycopg2-binary`.
*   Motor: PostgreSQL 15+.
*   Variables: Carga desde `.env` para máxima seguridad (GES-33).

---

## 2. Configuración en `settings.py`
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

---

## 3. Lógica de Transacciones (REQ-19)
Se ha implementado el uso de `@transaction.atomic` en la capa de servicios (`availability_service.py`) para asegurar que:
1.  La creación de disponibilidades sea atómica.
2.  El agendamiento de citas bloquee la fila para evitar "Race Conditions".
3.  Exista un roll-back automático en caso de fallo en la validación de negocio.

---

## 4. Implementación de Índices
Se han definido índices compuestos en los modelos para acelerar la agenda:
*   `disponibilidad`: Índice en `(medico, fecha)`.
*   `CitaMedica`: Índice en `(paciente, fecha_hora_cita)`.

---
*Documento de Ingeniería de Software - Sprint 2.*
