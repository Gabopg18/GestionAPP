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
