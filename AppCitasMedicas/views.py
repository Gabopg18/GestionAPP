# Contenido de views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .forms import CitaMedicaForm, disponibilidadMedicoForm, BuscarCitasForm, LoginMedicoForm , ReprogramarCitaForm, PacienteForm
from .models import CitaMedica, Medico, Paciente, disponibilidad
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST # Para solo aceptar POST
from django.http import JsonResponse
from datetime import datetime
from django.contrib.auth.views import LoginView
from django.utils.timezone import now


# Vistas Públicas (Pacientes)
def inicio_general(request):
    """Vista pública que oculta completamente la sesión médica"""
    return render(request, 'AppCitasMedicas/inicio_general.html', {
        'es_medico': False,
        'title': 'Sistema de Citas Médicas'
    })

def agendar_cita(request):
    if request.method == 'POST':
        paciente_form = PacienteForm(request.POST)
        cita_form = CitaMedicaForm(request.POST)

        if paciente_form.is_valid() and cita_form.is_valid():
            cd = paciente_form.cleaned_data
            paciente, creado = Paciente.objects.get_or_create(
                cedula=cd['cedula'],
                defaults={
                    'nombre': cd['nombre'],
                    'telefono': cd['telefono'],
                    'direccion': cd['direccion'],
                    'correo': cd['correo'],
                    'fecha_nacimiento': cd['fecha_nacimiento']
                }
            )
            if not creado:
                # Actualizar datos si ya existe
                paciente.nombre = cd['nombre']
                paciente.telefono = cd['telefono']
                paciente.direccion = cd['direccion']
                paciente.correo = cd['correo']
                paciente.fecha_nacimiento = cd['fecha_nacimiento']
                paciente.save()

            cita = cita_form.save(commit=False)
            cita.paciente = paciente
            cita.fecha_hora_cita = timezone.datetime.fromisoformat(cita_form.cleaned_data['fecha_hora_cita'])
            cita.save()

            messages.success(request, "Cita agendada correctamente.")
            return redirect('inicio_general')
        # Si no son válidos, mostrar los errores
        return render(request, 'AppCitasMedicas/agendar_cita.html', {
            'paciente_form': paciente_form,
            'cita_form': cita_form
        })

    else:
        paciente_form = PacienteForm()
        cita_form = CitaMedicaForm()

    return render(request, 'AppCitasMedicas/agendar_cita.html', {
        'paciente_form': paciente_form,
        'cita_form': cita_form
    })



def buscar_citas(request):
    """Vista para el formulario de búsqueda"""
    if request.method == 'POST':
        form = BuscarCitasForm(request.POST)
        if form.is_valid():
            cedula = form.cleaned_data['cedula']
            return redirect('ver_citas', cedula=cedula)
    else:
        form = BuscarCitasForm()
    
    return render(request, 'AppCitasMedicas/buscar_citas.html', {
        'form': form,
        'title': 'Buscar Mis Citas'
    })

def ver_citas(request, cedula):
    citas = CitaMedica.objects.filter(
    paciente__cedula=cedula,
    fecha_hora_cita__date__gte=now().date()
    ).order_by('fecha_hora_cita')
    # Depuración: Verificar IDs
    for cita in citas:
        if not hasattr(cita, 'id_cita') or not cita.id_cita:
            raise ValueError(f"Cita sin ID válido: {cita}")
    
    return render(request, 'AppCitasMedicas/ver_citas.html', {
        'citas': citas,
        'paciente': Paciente,
        'cedula': cedula
    })


def cancelar_cita(request, cita_id):
    cita = get_object_or_404(CitaMedica, id_cita=cita_id)
    ahora = timezone.now()

    if cita.estado != 'Agendada':
        messages.error(request, "Solo se pueden cancelar citas en estado 'Agendada'.")
        return redirect('ver_citas', cedula=cita.paciente.cedula)

    if (cita.fecha_hora_cita - ahora) < timedelta(hours=12):
        messages.error(request, "Solo se puede cancelar con al menos 12 horas de anticipación.")
        return redirect('ver_citas', cedula=cita.paciente.cedula)

    cita.estado = 'Cancelada'
    cita.save()
    messages.success(request, f"La cita con el Dr./Dra. {cita.medico.nombre} fue cancelada exitosamente.")
    return redirect('ver_citas', cedula=cita.paciente.cedula)

def reprogramar_cita(request, cita_id):
    cita = get_object_or_404(CitaMedica, id_cita=cita_id)
    ahora = timezone.now()

    # Check if the appointment can be rescheduled (12-hour rule)
    if (cita.fecha_hora_cita - ahora) < timedelta(hours=12):
        messages.error(request, 'Solo puedes reprogramar con más de 12 horas de anticipación.')
        return redirect('ver_citas', cedula=cita.paciente.cedula)

    if request.method == 'POST':
        form = ReprogramarCitaForm(request.POST, instance=cita)
        if form.is_valid():
            cita_reprogramada = form.save(commit=False)
            cita_reprogramada.estado = 'Reprogramada'
            cita_reprogramada.save()
            messages.success(request, 'La cita fue reprogramada exitosamente.')
            return redirect('ver_citas', cedula=cita.paciente.cedula)
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = ReprogramarCitaForm(instance=cita)

    return render(request, 'AppCitasMedicas/reprogramar_cita.html', {
        'form': form,
        'cita': cita,
        'title': 'Reprogramar Cita'
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
    
    # Obtener CITAS de esta semana
    citas_semana = CitaMedica.objects.filter(
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

def registrar_disponibilidad(request):
    if request.method == 'POST':
        form = disponibilidadMedicoForm(request.POST)
        if form.is_valid():
            nueva_disponibilidad = form.save(commit=False)
            nueva_disponibilidad.medico = request.user.medico
            
            # Verificar existencia usando el modelo directamente, no la instancia
            existe = disponibilidad.objects.filter(
                medico=nueva_disponibilidad.medico,
                fecha=nueva_disponibilidad.fecha,
                hora_inicio=nueva_disponibilidad.hora_inicio
            ).exists()
            
            if not existe:
                nueva_disponibilidad.save()
                messages.success(request, "Disponibilidad registrada correctamente.")
                return redirect('inicio_medico')
            else:
                messages.error(request, "Ya existe una disponibilidad para esta fecha y hora.")
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
    try:
        # Obtener la disponibilidad
        disp = get_object_or_404(
            disponibilidad,
            id=disponibilidad_id,
            medico=request.user.medico
        )
        
        if request.method == 'POST':
            form = disponibilidadMedicoForm(request.POST, instance=disp)
            if form.is_valid():
                # Verificar que no exista otra disponibilidad igual
                nueva_disp = form.save(commit=False)
                existe = disponibilidad.objects.filter(
                    medico=request.user.medico,
                    fecha=nueva_disp.fecha,
                    hora_inicio=nueva_disp.hora_inicio
                ).exclude(id=disp.id).exists()
                
                if not existe:
                    form.save()
                    messages.success(request, "Horario actualizado correctamente")
                    return redirect('ver_agenda_semanal')  # Redirigir a agenda semanal
                else:
                    messages.error(request, "Ya existe un horario para esta fecha y hora")
            else:
                messages.error(request, "Por favor corrige los errores en el formulario")
        else:
            form = disponibilidadMedicoForm(instance=disp)
        
        context = {
            'form': form,
            'disponibilidad': disp,
            'title': 'Editar Horario'
        }
        return render(request, 'AppCitasMedicas/editar_disponibilidad.html', context)
    
    except Exception as e:
        messages.error(request, f"Error al guardar cambios: {str(e)}")
        return redirect('ver_agenda_semanal')


@login_required
@user_passes_test(is_medico, login_url='registration/login')
@require_POST
def eliminar_disponibilidad(request, disponibilidad_id):
    disponibilidad = get_object_or_404(disponibilidad, id=disponibilidad_id, medico=request.user.medico)


    disponibilidad.delete()
    messages.success(request, "disponibilidad eliminada exitosamente.")
    return redirect('editar_disponibilidad') # Redirige a la lista de disponibilidades

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
    citas = CitaMedica.objects.filter(
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
                'fecha_hora_iso': fecha_hora_aware.isoformat(),
                'mostrar': f"{d.fecha.strftime('%d/%m/%Y')} - {d.hora_inicio.strftime('%H:%M')}",
                'fecha': d.fecha.strftime('%d/%m/%Y'),
                'hora': d.hora_inicio.strftime('%H:%M'),
                'medico_id': d.medico_id,
                'medico_nombre': str(d.medico)  
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