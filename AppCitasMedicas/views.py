# Contenido de views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.db.models import Count
from django.core.exceptions import ValidationError
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

from datetime import datetime, timedelta
import json

from .forms import CitaMedicaForm, disponibilidadMedicoForm, BuscarCitasForm, LoginMedicoForm , ReprogramarCitaForm, PacienteForm
from .models import CitaMedica, Medico, Paciente, disponibilidad
from .services.availability_service import AvailabilityService

@staff_member_required
def dashboard_admin(request):
    """Vista de analítica para administradores (REQ-18)"""
    # Estadísticas por estado
    stats_estado = CitaMedica.objects.values('estado').annotate(total=Count('estado'))
    
    # Estadísticas por especialidad
    stats_especialidad = CitaMedica.objects.values('medico__especialidad').annotate(total=Count('id_cita'))
    
    # Citas recientes
    citas_recientes = CitaMedica.objects.order_by('-fecha_creacion')[:5]

    context = {
        'stats_estado': stats_estado,
        'stats_especialidad': stats_especialidad,
        'citas_recientes': citas_recientes,
        'total_citas': CitaMedica.objects.count(),
        'total_pacientes': Paciente.objects.count(),
    }
    return render(request, 'AppCitasMedicas/dashboard_admin.html', context)
from django.views.decorators.http import require_GET, require_POST
from .services.pdf_service import PDFService

@require_GET
def generar_pdf_cita(request, cita_id):
    """Genera un comprobante de cita en formato PDF (REQ-17)"""
    return PDFService.generar_comprobante_cita(cita_id)

# Vistas Públicas (Pacientes)
def inicio_general(request):
    """Vista pública que oculta completamente la sesión médica"""
    return render(request, 'AppCitasMedicas/inicio_general.html', {
        'es_medico': False,
        'title': 'Sistema de Citas Médicas'
    })

class AgendarCitaView(View):
    """Vista basada en clases para agendar citas (REQ-02)"""
    template_name = 'AppCitasMedicas/agendar_cita.html'

    def get(self, request):
        return render(request, self.template_name, {
            'paciente_form': PacienteForm(),
            'cita_form': CitaMedicaForm()
        })

    def post(self, request):
        paciente_form = PacienteForm(request.POST)
        cita_form = CitaMedicaForm(request.POST)

        if paciente_form.is_valid() and cita_form.is_valid():
            cd = paciente_form.cleaned_data
            
            try:
                with transaction.atomic():
                    # 1. Gestionar Paciente
                    paciente, _ = Paciente.objects.update_or_create(
                        cedula=cd['cedula'],
                        defaults={
                            'nombre': cd['nombre'],
                            'telefono': cd['telefono'],
                            'direccion': cd['direccion'],
                            'correo': cd['correo'],
                            'fecha_nacimiento': cd['fecha_nacimiento']
                        }
                    )

                    # 2. Obtener Disponibilidad y Agendar vía Servicio
                    dispo_id = cita_form.cleaned_data['fecha_hora_cita']
                    dispo_obj = get_object_or_404(disponibilidad, id=dispo_id)
                    
                    AvailabilityService.book_appointment(paciente, dispo_obj)
                    messages.success(request, "¡Cita agendada con éxito!")
                    return redirect('inicio_general')
                    
            except ValidationError as e:
                messages.error(request, f"Error: {e.message}")
            except Exception as e:
                messages.error(request, f"Error inesperado: {str(e)}")

        return render(request, self.template_name, {
            'paciente_form': paciente_form,
            'cita_form': cita_form
        })





class BuscarCitasView(View):
    """Vista basada en clases para el formulario de búsqueda (REQ-03)"""
    template_name = 'AppCitasMedicas/buscar_citas.html'

    def get(self, request):
        form = BuscarCitasForm()
        return render(request, self.template_name, {
            'form': form,
            'title': 'Buscar Mis Citas'
        })

    def post(self, request):
        form = BuscarCitasForm(request.POST)
        if form.is_valid():
            cedula = form.cleaned_data['cedula']
            return redirect('ver_citas', cedula=cedula)
        return render(request, self.template_name, {'form': form})

class VerCitasView(View):
    """Vista basada en clases para listar citas (REQ-04)"""
    template_name = 'AppCitasMedicas/ver_citas.html'

    def get(self, request, cedula):
        # Usamos el Manager para encapsular la lógica de filtrado
        citas = CitaMedica.objects.activas_paciente(cedula)
        
        return render(request, self.template_name, {
            'citas': citas,
            'cedula': cedula
        })


def cancelar_cita(request, cita_id):
    """Confirmación y cancelación de cita (REQ-05)"""
    cita = get_object_or_404(CitaMedica, id_cita=cita_id)
    ahora = timezone.now()

    if request.method == 'POST':
        if cita.estado != 'Pendiente':
            messages.error(request, "Solo se pueden cancelar citas en estado 'Pendiente'.")
            return redirect('ver_citas', cedula=cita.paciente.cedula)

        if (cita.fecha_hora_cita - ahora) < timedelta(hours=12):
            messages.error(request, "Solo se puede cancelar con al menos 12 horas de anticipación.")
            return redirect('ver_citas', cedula=cita.paciente.cedula)

        cita.estado = 'Cancelada'
        cita.save()
        messages.success(request, "Cita cancelada exitosamente.")
        return redirect('ver_citas', cedula=cita.paciente.cedula)

    return render(request, 'AppCitasMedicas/cancelar_cita.html', {'cita': cita})

def reprogramar_cita(request, cita_id):
    """Permite cambiar la fecha de una cita existente (REQ-05)"""
    cita = get_object_or_404(CitaMedica, id_cita=cita_id)
    ahora = timezone.now()

    # Validación de las 12 horas
    if (cita.fecha_hora_cita - ahora) < timedelta(hours=12):
        messages.error(request, 'Solo puedes reprogramar con más de 12 horas de anticipación.')
        return redirect('ver_citas', cedula=cita.paciente.cedula)
    
    if request.method == 'POST':
        form = ReprogramarCitaForm(request.POST, instance=cita)
        if form.is_valid():
            nueva_dispo_id = form.cleaned_data['nueva_disponibilidad']
            nueva_dispo = get_object_or_404(disponibilidad, id=nueva_dispo_id)
            
            try:
                with transaction.atomic():
                    # 1. Agendar la nueva usando el servicio
                    AvailabilityService.book_appointment(cita.paciente, nueva_dispo, cita.notas_paciente)
                    
                    # 2. Cancelar la cita vieja
                    cita.estado = 'Cancelada'
                    cita.notas_paciente += " (Reprogramada)"
                    cita.save()
                    
                    messages.success(request, "Cita reprogramada exitosamente.")
                    return redirect('ver_citas', cedula=cita.paciente.cedula)
            except ValidationError as e:
                messages.error(request, f"Error: {e.message}")
    else:
        form = ReprogramarCitaForm(instance=cita)
    
    return render(request, 'AppCitasMedicas/reprogramar_cita.html', {
        'form': form,
        'cita': cita
    })


# Vistas Médicos (requieren login)
def is_medico(user):
    return hasattr(user, 'Medico') and user.medico.id is not None or user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_medico, login_url='registration/login')
def inicio_medico(request):
    """Vista exclusiva para médicos muestra opciones completas"""
    return render(request, 'AppCitasMedicas/inicio_medico.html', {
        'es_medico': True,
        'title': 'Panel Médico'
    })

@login_required
@user_passes_test(is_medico, login_url='registration/login')
def ver_agenda_medica (request):
    # Obtener el médico logueado
    medico = request.user.medico
    
    # Calcular fechas de la semana actual
    hoy = timezone.now().date()
    inicio_semana = hoy - timedelta(days=hoy.weekday())  # Lunes de esta semana
    fin_semana = inicio_semana + timedelta(days=6)       # Domingo de esta semana
    
    # Obtener CITAS de esta semana (Optimizado con select_related)
    citas_semana = CitaMedica.objects.select_related('paciente').filter(
        medico=medico,
        fecha_hora_cita__date__range=[inicio_semana, fin_semana]
    ).order_by('fecha_hora_cita')
    
    # Obtener DISPONIBILIDADES de esta semana
    disponibilidades_semana = disponibilidad.objects.filter(
        medico=medico,
        fecha__range=[inicio_semana, fin_semana]
    ).order_by('fecha', 'hora_inicio')
    
    # Preparar datos combinados para la plantilla
    agenda_semanal = []
    
    # Agregar disponibilidades primero
    for disp in disponibilidades_semana:
        agenda_semanal.append({
            'tipo': 'disponibilidad',
            'id': disp.id,
            'fecha': disp.fecha,
            'hora': disp.hora_inicio,
            'hora_fin': disp.hora_fin,
            'ocupado': False  # Marcador para disponibilidad
        })
    
    # Agregar citas
    for cita in citas_semana:
        agenda_semanal.append({
            'tipo': 'cita',
            'id': cita.id_cita,
            'fecha': cita.fecha_hora_cita.date(),
            'hora': cita.fecha_hora_cita.time(),
            'paciente': cita.paciente,
            'estado': cita.get_estado_display(),
            'estado_raw': cita.estado,
            'ocupado': True  # Marcador para cita
        })
    
    # Ordenar por fecha y hora
    agenda_semanal.sort(key=lambda x: (x['fecha'], x['hora']))
    
    context = {
        'agenda_semanal': agenda_semanal,
        'title': 'Mi Agenda Semanal',
        'inicio_semana': inicio_semana,
        'fin_semana': fin_semana
    }
    return render(request, 'AppCitasMedicas/ver_agenda_semanal.html', context)

@login_required
@user_passes_test(is_medico, login_url='registration/login')
def calendario_interactivo(request):
    """Vista para el calendario interactivo con FullCalendar"""
    return render(request, 'AppCitasMedicas/calendario_medico.html', {
        'title': 'Calendario Interactivo',
        'medico': request.user.medico
    })

@login_required
@user_passes_test(is_medico, login_url='registration/login')
def registrar_disponibilidad(request):
    """Vista para registrar disponibilidad usando el Service Layer (REQ-19)"""
    if request.method == 'POST':
        form = disponibilidadMedicoForm(request.POST)
        if form.is_valid():
            try:
                # Delegamos la validación y creación al servicio profesional
                AvailabilityService.validate_and_create(
                    medico=request.user.medico,
                    fecha=form.cleaned_data['fecha'],
                    hora_inicio=form.cleaned_data['hora_inicio'],
                    hora_fin=form.cleaned_data['hora_fin']
                )
                messages.success(request, "Disponibilidad registrada correctamente.")
                return redirect('inicio_medico')
            except ValidationError as e:
                # Capturamos los errores de negocio lanzados por el servicio
                messages.error(request, f"Error: {e.message}")
            except Exception as e:
                messages.error(request, f"Error inesperado: {str(e)}")
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        form = disponibilidadMedicoForm()
    
    return render(request, 'AppCitasMedicas/registrar_disponibilidad.html', {
        'form': form,
        'title': 'Registrar Disponibilidad'
    })

@login_required
@user_passes_test(is_medico, login_url='registration/login')
def editar_disponibilidad(request, disponibilidad_id):
    """Vista para editar disponibilidad usando el Service Layer (REQ-19)"""
    disp_obj = get_object_or_404(disponibilidad, id=disponibilidad_id, medico=request.user.medico)
    
    if request.method == 'POST':
        form = disponibilidadMedicoForm(request.POST, instance=disp_obj)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Para validar sin chocar con el registro actual, usamos el servicio
                    # Primero validamos que el nuevo rango sea aceptable (excluyendo el actual)
                    # En una arquitectura real, el servicio manejaría el 'exclude(id=...)'.
                    # Por simplicidad, aquí validamos y luego actualizamos.
                    AvailabilityService.validate_and_create(
                        medico=request.user.medico,
                        fecha=form.cleaned_data['fecha'],
                        hora_inicio=form.cleaned_data['hora_inicio'],
                        hora_fin=form.cleaned_data['hora_fin']
                    )
                    disp_obj.delete() # Reemplazo exitoso
                
                messages.success(request, "Horario actualizado correctamente.")
                return redirect('inicio_medico')
            except ValidationError as e:
                messages.error(request, f"Error: {e.message}")
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = disponibilidadMedicoForm(instance=disp_obj)
    
    return render(request, 'AppCitasMedicas/registrar_disponibilidad.html', {
        'form': form,
        'title': 'Editar Horario'
    })

@login_required
@user_passes_test(is_medico, login_url='registration/login')
def eliminar_disponibilidad(request, disponibilidad_id):
    """Confirmación y eliminación segura de disponibilidad (REQ-19)"""
    disp_obj = get_object_or_404(disponibilidad, id=disponibilidad_id, medico=request.user.medico)
    
    if request.method == 'POST':
        try:
            AvailabilityService.delete_safe(disp_obj)
            messages.success(request, "Disponibilidad eliminada exitosamente.")
            return redirect('inicio_medico')
        except ValidationError as e:
            messages.error(request, f"Error: {e.message}")
            return redirect('inicio_medico')

    return render(request, 'AppCitasMedicas/eliminar_disponibilidad.html', {'disponibilidad': disp_obj})

# Autenticación
def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginMedicoForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"¡Bienvenido, {user.username}!")
                # Redirigir al panel de médico si el usuario es un médico
                if hasattr(user, 'medico') or user.is_staff or user.is_superuser:
                    return redirect('inicio_medico')
                # Si no es médico, podrías redirigir a otro lado o dar un error
                messages.error(request, "Tu cuenta no tiene acceso a esta sección.")
                logout(request) # Cerrar sesión si no es el tipo de usuario esperado
                return redirect('registration/login') # Redirigir al login de nuevo
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        else:
            # Los errores del formulario se mostrarán en el template
            pass 
    else:
        form = LoginMedicoForm()
    return render(request, 'AppCitasMedicas/login.html', {'form': form})

@login_required
def mis_citas_medico(request):
    """
    Vista para que el médico vea todas sus citas
    """
    # Obtener el médico logueado
    medico = request.user.medico
    
    # Obtener todas las citas del médico, ordenadas por fecha descendente
    citas = CitaMedica.objects.select_related('paciente').filter(
        medico=medico
    ).order_by('-fecha_hora_cita')
    
    context = {
        'citas': citas,
        'title': 'Mis Citas Médicas'
    }
    return render(request, 'AppCitasMedicas/mis_citas_medico.html', context)

@login_required
def cerrar_sesion(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('inicio_general')

# Otras Vistas
def confirmacion_disponibilidad(request):
    """Vista de confirmación después de registrar disponibilidad"""
    return render(request, 'AppCitasMedicas/confirmacion_disponibilidad.html', {
        'title': 'disponibilidad Registrada'
    })


@require_GET
def obtener_disponibilidades(request):
    """
    API endpoint that returns available time slots for a doctor in JSON format.
    
    Args:
        request: HttpRequest with 'medico_id' GET parameter
        
    Returns:
        JsonResponse: List of available time slots or error message
        
    Example success response:
        [{
            "id": 1,
            "fecha_hora_iso": "2023-12-15T09:00:00-04:00",
            "mostrar": "15/12/2023 - 09:00",
            "fecha": "15/12/2023",
            "hora": "09:00"
        }]
        
    Example error response:
        {"error": "Invalid doctor ID", "status": 400}
    """
    medico_id = request.GET.get('medico_id')
    
 
    if not medico_id or not medico_id.isdigit():
        return JsonResponse(
            {'error': 'Se requiere un ID de médico válido', 'status': 400},
            status=400
        )

    try:

        ahora = timezone.now()
        disponibilidades = disponibilidad.objects.filter(
            medico_id=medico_id,
            fecha__gte=ahora.date()
        ).exclude(
            fecha=ahora.date(),
            hora_inicio__lt=ahora.time()
        ).order_by('fecha', 'hora_inicio')

        resultados = []
        for d in disponibilidades:

            fecha_hora = timezone.datetime.combine(d.fecha, d.hora_inicio)
            fecha_hora_aware = timezone.make_aware(fecha_hora)
            
            resultados.append({
                'id': d.id,
                'title': 'Disponible',
                'start': timezone.datetime.combine(d.fecha, d.hora_inicio).isoformat(),
                'end': timezone.datetime.combine(d.fecha, d.hora_fin).isoformat(),
                'fecha': d.fecha.strftime('%d/%m/%Y'),
                'hora': d.hora_inicio.strftime('%H:%M'),
                'medico_id': d.medico_id,
                'medico_nombre': str(d.medico),
                'color': '#28a745' # Verde para disponible
            })

        return JsonResponse(resultados, safe=False)

    except Exception as e:
        return JsonResponse(
            {'error': 'Error al obtener disponibilidades', 'details': str(e), 'status': 500},
            status=500
        )
    


class LoginMedicoView(LoginView):
    template_name = 'AppCitasMedicas/login.html'
    authentication_form = LoginMedicoForm

@require_GET
def obtener_medicos(request):
    """
    API endpoint para obtener médicos, con opción de filtrado por especialidad.
    """
    especialidad = request.GET.get('especialidad')
    
    if especialidad:
        # Filtrado insensible a mayúsculas y minúsculas
        medicos = Medico.objects.filter(especialidad__iexact=especialidad)
    else:
        medicos = Medico.objects.all()
        
    resultados = []
    for m in medicos:
        resultados.append({
            'id': m.user.id,
            'nombre': m.user.get_full_name() or m.user.username,
            'especialidad': m.especialidad
        })
        
    return JsonResponse(resultados, safe=False)