# 🧪 Estrategia de Pruebas - Sprint 2

**Responsable:** Juan Sebastián Mayorga (Ingeniero de Calidad)  
**Proyecto:** GestionAPP  

---

## 1. Nuevos Objetivos de Prueba
Para el Sprint 2, la calidad se centrará en la **integridad de la API** y la **fidelidad de los documentos generados**.

### A. Pruebas de API REST (REQ-16)
*   **Herramientas:** `Pytest` + `Django REST Framework Testing`.
*   **Validaciones:**
    *   Verificar que los endpoints devuelven códigos `200 OK` y `201 Created`.
    *   Validar que los datos sensibles no se expongan en el JSON.
    *   Pruebas de autenticación por Token.

### B. Pruebas de Generación de PDF (REQ-17)
*   **Validaciones:**
    *   Verificar que el archivo PDF se genera sin errores de renderizado.
    *   Asegurar que los datos del paciente en el PDF coinciden con la BD.
    *   Prueba de descarga en diferentes navegadores.

---

## 2. Actualización de Pruebas de Carga (Locust)
Se añadirá una tarea al script de Locust para probar la concurrencia en la API:
```python
@task
def test_api_list_appointments(self):
    self.client.get("/api/citas/", headers={"Authorization": "Token [token_id]"})
```

---

## 3. Criterios de Aceptación de Calidad (Sprint 2)
- [ ] Cobertura de pruebas en Serializers > 90%.
- [ ] Tiempo de generación de PDF < 3 segundos.
- [ ] API documentada con Swagger o ReDoc (Opcional pero recomendado).

---
*Plan de QA para el Sprint 2 - GestionAPP.*
