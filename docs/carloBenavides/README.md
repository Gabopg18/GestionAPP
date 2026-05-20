# GestionAPP - Citas Médicas

Este es un proyecto desarrollado en Django para la gestión de citas médicas, pacientes y disponibilidades de médicos.

## Requerimientos Funcionales

A continuación se detallan los requerimientos funcionales del sistema:

| ID | Nombre | Descripción | Entradas | Resultados |
| :---: | :--- | :--- | :--- | :--- |
| **REQ-01** | Iniciar sesión | Permitir a los usuarios (médicos o personal administrativo) acceder al sistema de forma segura para gestionar las citas y agendas. | Nombre de usuario y contraseña. | El sistema verifica los datos y, si son correctos, da acceso a las funciones correspondientes al usuario. Si no lo son, muestra un mensaje de error. |
| **REQ-02** | Recuperar contraseña | Permitir a un usuario que ha olvidado su contraseña restablecerla mediante un enlace seguro enviado a su correo electrónico. | Correo electrónico del usuario registrado. | El sistema envía un correo con un enlace temporal. Al hacer clic en el enlace, el usuario ingresa una nueva contraseña, y el sistema la guarda actualizada. |
| **REQ-03** | Buscar citas de paciente | Permitir consultar todas las citas que un paciente específico tiene agendadas o ha tenido en el pasado utilizando su número de identificación. | Número de identificación (cédula) del paciente. | El sistema busca al paciente y muestra una lista con todas las citas médicas asociadas a él, indicando su estado, fecha, hora y el médico asignado. |
| **REQ-04** | Agendar cita | Permitir reservar un espacio disponible en la agenda de un médico para que un paciente asista a una consulta. | Datos del paciente (cédula, nombre, teléfono), el médico seleccionado, y la fecha/hora elegida de acuerdo a los espacios libres. | El sistema guarda la cita, le asigna el estado "Agendada", ocupa ese espacio en el horario del médico y genera la confirmación de la reserva. |
| **REQ-05** | Cancelar cita | Permitir anular una cita que ya estaba programada, de manera que el espacio quede nuevamente libre para otro paciente. | La cita específica a cancelar (identificador) y un motivo de cancelación (opcional). | El sistema cambia el estado de la cita a "Cancelada", registra quién la canceló, y libera el horario en la agenda del médico. |
| **REQ-06** | Reprogramar cita | Permitir cambiar la fecha y la hora de una cita ya existente por un nuevo horario que esté disponible. | La cita actual a modificar y la nueva fecha/hora elegida. | El sistema actualiza la cita para el nuevo horario, reserva el nuevo espacio y deja libre el espacio que ocupaba anteriormente. |
| **REQ-07** | Ver agenda médica | Permitir a los médicos visualizar de forma organizada todas las citas que tienen programadas para su jornada o semana. | (Opcional) Selección de la fecha, día o semana a visualizar. | El sistema muestra una vista detallada (lista o calendario) con todas las citas asignadas a ese médico, mostrando los detalles de los pacientes a atender. |
| **REQ-08** | Registrar disponibilidad | Permitir al médico definir los bloques de horarios en los días que estará disponible para recibir citas de pacientes. | Fecha, hora de inicio y hora de fin del bloque disponible. | El sistema guarda este horario como libre en la agenda del médico, permitiendo desde ese momento que se agenden citas en ese periodo. |
| **REQ-09** | Editar disponibilidad | Permitir modificar un bloque de horario disponible que ya había sido registrado por el médico. | El bloque de horario a modificar, la nueva hora de inicio o la nueva hora de fin. | El sistema actualiza el horario con los nuevos límites de tiempo, siempre y cuando el nuevo rango no afecte citas que ya hayan sido agendadas en ese lapso. |
| **REQ-10** | Eliminar disponibilidad | Permitir a un médico borrar un bloque de tiempo de su agenda para indicar que ya no estará disponible para recibir citas en ese lapso. | El bloque de horario específico que se desea borrar. | El sistema elimina ese espacio de tiempo de la agenda, evitando que se puedan agendar nuevas citas en ese momento. |
| **REQ-11** | Enviar recordatorios | Permitir al sistema notificar a los pacientes sobre la cercanía de sus citas programadas para disminuir la inasistencia. | Cita médica que está próxima a ocurrir (incluyendo el medio de envío seleccionado, como correo electrónico). | El sistema genera y envía el mensaje al paciente recordando el día, la hora y el médico, y marca el recordatorio como "Enviado" en la base de datos. |
# Criterios de Aceptación

**REQ‑01 – Iniciar sesión**
| # | Given‑When‑Then | Resultado esperado |
|---|-----------------|--------------------|
| 1 | **Given** usuario con credenciales válidas.<br>**When** ingresa usuario y contraseña y pulsa "Entrar".<br>**Then** se redirige al panel principal y muestra su nombre. | Acceso exitoso al sistema. |
| 2 | **Given** credenciales inválidas.<br>**When** intenta iniciar sesión.<br>**Then** muestra mensaje de error *"Credenciales incorrectas"*. | Acceso denegado. |

**REQ‑02 – Recuperar contraseña**
| # | Given‑When‑Then | Resultado esperado |
|---|-----------------|--------------------|
| 1 | **Given** usuario registrado con email válido.<br>**When** solicita recuperación de contraseña.<br>**Then** se envía email con enlace de restablecimiento. | Email enviado con link. |
| 2 | **Given** enlace expirado.<br>**When** intenta usarlo.<br>**Then** muestra mensaje *"Enlace no válido o expirado"*. | Restablecimiento fallido. |

**REQ‑03 – Buscar citas de paciente**
| # | Given‑When‑Then | Resultado esperado |
|---|-----------------|--------------------|
| 1 | **Given** número de cédula del paciente.<br>**When** busca sus citas.<br>**Then** se listan todas sus citas con estado y detalle. | Lista mostrada. |
| 2 | **Given** cédula inexistente.<br>**When** busca.<br>**Then** muestra mensaje *"Paciente no encontrado"*. |

**REQ‑04 – Agendar cita**
| # | Given‑When‑Then | Resultado esperado |
|---|-----------------|--------------------|
| 1 | **Given** médico con disponibilidad y datos del paciente.<br>**When** reserva la cita.<br>**Then** la cita se crea con estado "Agendada" y espacio queda ocupado. | Cita creada. |
| 2 | **Given** horario sin disponibilidad.<br>**When** intenta agendar.<br>**Then** muestra error *"No hay plazas disponibles"*. |

**REQ‑05 – Cancelar cita**
| # | Given‑When‑Then | Resultado esperado |
|---|-----------------|--------------------|
| 1 | **Given** cita en estado "Pendiente".<br>**When** se pulsa "Cancelar".<br>**Then** el estado cambia a "Cancelada" y se libera el horario. | Cita cancelada. |
| 2 | **Given** cita con menos de 12 h restantes.<br>**When** intenta cancelar.<br>**Then** muestra error *"No se puede cancelar dentro de 12 h"*. |

**REQ‑06 – Reprogramar cita**
| # | Given‑When‑Then | Resultado esperado |
|---|-----------------|--------------------|
| 1 | **Given** cita existente y nuevo horario disponible.<br>**When** reprograma la cita.<br>**Then** la cita se actualiza al nuevo tiempo y el anterior queda libre. | Cita reprogramada. |
| 2 | **Given** nuevo horario conflictivo.<br>**When** intenta reprogramar.<br>**Then** muestra error *"Horario no disponible"*. |

**REQ‑07 – Ver agenda médica**
| # | Given‑When‑Then | Resultado esperado |
|---|-----------------|--------------------|
| 1 | **Given** médico autenticado.<br>**When** accede a su agenda.<br>**Then** se muestra lista o calendario con todas sus citas y estados. | Agenda visible. |

**REQ‑08 – Registrar disponibilidad**
| # | Given‑When‑Then | Resultado esperado |
|---|-----------------|--------------------|
| 1 | **Given** médico y rango de horario.
**When** guarda disponibilidad.
**Then** el bloque queda registrado como libre para citas. | Disponibilidad añadida. |
| 2 | **Given** horario que se solapa con disponibilidad existente.<br>**When** intenta registrar.
**Then** muestra error *"Superposición de disponibilidad"*. |

**REQ‑09 – Editar disponibilidad**
| # | Given‑When‑Then | Resultado esperado |
|---|-----------------|--------------------|
| 1 | **Given** que el médico tiene una disponibilidad de 09:00‑10:00 el 11/05/2026.<br>**When** cambia la hora de fin a 10:30.<br>**Then** la disponibilidad se actualiza a 09:00‑10:30 y muestra *"Disponibilidad actualizada correctamente"*. | Horario actualizado en BD. |
| 2 | **Given** que existen citas entre 09:30‑10:00.<br>**When** intenta mover la hora de fin a 09:45.<br>**Then** el sistema rechaza la edición con mensaje *"No es posible modificar la disponibilidad porque existen citas programadas"*. | No se modifica. |
| 3 | **Given** que la disponibilidad pertenece a otro médico.<br>**When** intenta editarla.<br>**Then** se deniega el acceso con mensaje *"No tiene permiso para editar esta disponibilidad"*. | Seguridad. |

**REQ‑10 – Eliminar disponibilidad**
| # | Given‑When‑Then | Resultado esperado |
|---|-----------------|--------------------|
| 1 | **Given** disponibilidad 14:00‑15:00.<br>**When** confirma eliminación.<br>**Then** se elimina y se muestra *"Disponibilidad eliminada"*. | Registro borrado. |
| 2 | **Given** citas agendadas dentro del bloque.<br>**When** intenta eliminar.<br>**Then** muestra error *"No se puede eliminar la disponibilidad porque hay citas programadas"*. | No se elimina. |
| 3 | **Given** médico intenta eliminar disponibilidad de otro médico.<br>**When** accede a la URL.<br>**Then** mensaje *"No tiene permiso"*. | Seguridad. |

**REQ‑11 – Enviar recordatorios**
| # | Given‑When‑Then | Resultado esperado |
|---|-----------------|--------------------|
| 1 | **Given** cita mañana a 10:00 con email.<br>**When** corre job.
**Then** se envía email y registro marca *Enviado*. | Email entregado. |
| 2 | **Given** cita con teléfono y preferencia SMS.<br>**When** corre job.
**Then** se envía SMS y marca *Enviado*. | SMS entregado. |
| 3 | **Given** servidor de correo caído.
**When** intenta enviar.
**Then** registra error y marca *Fallido* para reintentar. | Manejo de fallos. |


**REQ‑09 – Editar disponibilidad**

| # | Given‑When‑Then | Resultado esperado |
|---|-----------------|--------------------|
| 1 | **Given** que el médico tiene una disponibilidad de 09:00‑10:00 el 11/05/2026. **When** cambia la hora de fin a 10:30. **Then** la disponibilidad se actualiza a 09:00‑10:30 y muestra *"Disponibilidad actualizada correctamente"*. | Horario actualizado en BD. |
| 2 | **Given** que existen citas entre 09:30‑10:00. **When** intenta mover la hora de fin a 09:45. **Then** el sistema rechaza la edición con mensaje *"No es posible modificar la disponibilidad porque existen citas programadas"*. | No se modifica. |
| 3 | **Given** que la disponibilidad pertenece a otro médico. **When** intenta editarla. **Then** se deniega el acceso con mensaje *"No tiene permiso para editar esta disponibilidad"*. | Seguridad. |

**REQ‑10 – Eliminar disponibilidad**

| # | Given‑When‑Then | Resultado esperado |
|---|-----------------|--------------------|
| 1 | **Given** disponibilidad 14:00‑15:00. **When** confirma eliminación. **Then** se elimina y se muestra *"Disponibilidad eliminada"*. | Registro borrado. |
| 2 | **Given** citas agendadas dentro del bloque. **When** intenta eliminar. **Then** muestra error *"No se puede eliminar la disponibilidad porque hay citas programadas"*. | No se elimina. |
| 3 | **Given** médico intenta eliminar disponibilidad de otro médico. **When** accede a la URL. **Then** mensaje *"No tiene permiso"*. | Seguridad. |

**REQ‑11 – Enviar recordatorios**

| # | Given‑When‑Then | Resultado esperado |
|---|-----------------|--------------------|
| 1 | **Given** cita mañana a 10:00 con email. **When** corre job. **Then** se envía email y registro marca *Enviado*. | Email entregado. |
| 2 | **Given** cita con teléfono y preferencia SMS. **When** corre job. **Then** se envía SMS y marca *Enviado*. | SMS entregado. |
| 3 | **Given** servidor de correo caído. **When** intenta enviar. **Then** registra error y marca *Fallido* para reintentar. | Manejo de fallos. |

## Requerimientos No Funcionales
## Requerimientos No Funcionales

A continuación se detallan los requerimientos no funcionales del sistema, basados en el estándar de calidad de software ISO/IEC 25010:

| ID | Nombre | Métricas ISO/IEC 25010 | Descripción |
| :---: | :--- | :--- | :--- |
| **RNF-01** | Velocidad de respuesta | Eficiencia de desempeño (Comportamiento temporal) | El sistema debe cargar las vistas y procesar las solicitudes (como agendar o buscar una cita) en un tiempo máximo de 2 segundos bajo condiciones normales de red. |
| **RNF-02** | Seguridad de contraseñas | Seguridad (Confidencialidad) | Las contraseñas de los usuarios deben almacenarse de forma encriptada mediante algoritmos robustos (ej. PBKDF2), evitando que se puedan leer en texto plano en la base de datos. |
| **RNF-03** | Compatibilidad de navegadores | Compatibilidad (Interoperabilidad) | La interfaz de usuario debe funcionar correctamente y sin distorsión visual en las versiones más recientes de los navegadores web modernos (Chrome, Firefox, Safari, Edge). |
| **RNF-04** | Diseño responsivo | Usabilidad (Operabilidad) | El diseño de las pantallas debe adaptarse correctamente a diferentes tamaños de pantalla, garantizando su uso tanto en computadoras de escritorio como en dispositivos móviles. |
| **RNF-05** | Protección de datos sensibles | Seguridad (Integridad / Confidencialidad) | Solo los usuarios autorizados (médicos o administradores autenticados) pueden acceder a la información de contacto y al historial de citas de los pacientes. |
| **RNF-06** | Facilidad de mantenimiento | Mantenibilidad (Modularidad) | El código fuente debe estar estructurado siguiendo la arquitectura MVT de Django y mantener una separación clara de responsabilidades para facilitar futuras actualizaciones. |
| **RNF-07** | Alta disponibilidad | Fiabilidad (Disponibilidad) | El sistema debe mantenerse operativo y accesible al menos un 99.5% del tiempo durante los horarios establecidos de atención de la clínica. |
| **RNF-08** | Portabilidad a servidores | Portabilidad (Instalabilidad) | La aplicación debe estar estructurada de manera que pueda ser desplegada en diferentes plataformas (ej. AWS, Heroku, servidores Linux) que soporten Python y Django, sin requerir grandes cambios en el código. |

## Criterios de Evaluación de Requerimientos No Funcionales

| ID | Métrica | Umbral / Valor esperado |
|---|---|---|
| RNF-01 | Tiempo de respuesta de página | ≤ 2 s bajo carga normal |
| RNF-02 | Almacenamiento de contraseñas | Hash con PBKDF2 (mínimo 12 000 iteraciones) |
| RNF-03 | Compatibilidad de navegadores | Chrome ≥ 89, Firefox ≥ 86, Safari ≥ 14, Edge ≥ 89 |
| RNF-04 | Diseño responsivo | Pruebas en resoluciones 320 px‑1920 px sin desbordes |
| RNF-05 | Protección de datos | Encriptado TLS 1.2+ para datos en tránsito, cifrado AES‑256 para datos sensibles |
| RNF-06 | Mantenibilidad | Cobertura de pruebas unitarias ≥ 80 % y lint sin errores críticos |
| RNF-07 | Disponibilidad | Uptime ≥ 99.5 % mensual (excluyendo mantenimiento planificado) |
| RNF-08 | Portabilidad | Deploy en al menos 2 entornos diferentes (AWS + Heroku) sin cambios de código |

