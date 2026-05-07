from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views, api_views

router = DefaultRouter()
router.register(r'disponibilidades', api_views.DisponibilidadViewSet)
router.register(r'citas', api_views.CitaMedicaViewSet)

 

urlpatterns = [
    # API REST (Sprint 2) - Accesible en /api/
    path('api/', include(router.urls)),
    path('admin/dashboard/', views.dashboard_admin, name='dashboard_admin'),

    # Vistas Generales - Ahora esta será la raíz (/)
    path('', views.inicio_general, name='inicio_general'),
    
    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='registration/login'),
    path('logout/', views.cerrar_sesion, name='registration/logout'), # Usar la vista personalizada
    
    # Pacientes
    path('buscar-citas/', views.BuscarCitasView.as_view(), name='buscar_citas'),
    path('ver-citas/<str:cedula>/', views.VerCitasView.as_view(), name='ver_citas'),
    path('citas/agendar/', views.AgendarCitaView.as_view(), name='agendar_cita'),
    path('citas/comprobante/<uuid:cita_id>/', views.generar_pdf_cita, name='generar_pdf_cita'),
    path('citas/cancelar/<uuid:cita_id>/', views.cancelar_cita, name='cancelar_cita'),
    path('citas/reprogramar/<uuid:cita_id>/', views.reprogramar_cita, name='reprogramar_cita'),
    
    # Médicos
    path('medico/', views.inicio_medico, name='inicio_medico'),
    path('medico/agenda/', views.ver_agenda_medica, name='ver_agenda_semanal'),
    path('medico/calendario/', views.calendario_interactivo, name='calendario_interactivo'),
    path('medico/disponibilidad/registrar/', views.registrar_disponibilidad, name='registrar_disponibilidad'),
    path('ajax/disponibilidades/', views.obtener_disponibilidades, name='ajax_disponibilidades'),
    path('mis-citas-medico/', views.mis_citas_medico, name='mis_citas_medico'),
    path('medicos/', views.obtener_medicos, name='obtener_medicos'),
    

    
    # URLs para editar y eliminar una disponibilidad específica
    path('medico/disponibilidad/<int:disponibilidad_id>/editar/', 
         views.editar_disponibilidad, name='editar_disponibilidad'), 
    path('medico/disponibilidad/<int:disponibilidad_id>/eliminar/', 
         views.eliminar_disponibilidad, name='eliminar_disponibilidad'), 
         
    path('medico/confirmacion/', views.confirmacion_disponibilidad, name='confirmacion_disponibilidad'),
    
    # Recuperación de contraseña (Ajuste de template_name para coincidir con los que te proporcioné)
    path('recuperar-contraseña/',
         auth_views.PasswordResetView.as_view(
             template_name='AppCitasMedicas/recuperar_contraseña.html', # Nombre de template ajustado
             email_template_name='AppCitasMedicas/email_recuperacion.html', # Asegúrate de crear este template para el correo
             subject_template_name='AppCitasMedicas/recuperar_contraseña_subject.txt', # Asegúrate de crear este archivo para el asunto
             success_url='/recuperar-contraseña/enviado/'
         ),
         name='password_reset'),
    
    path('recuperar-contraseña/enviado/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='AppCitasMedicas/recuperar_contraseña_enviado.html'
         ),
         name='password_reset_done'),
    
    path('recuperar-contraseña/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='AppCitasMedicas/nueva_contraseña.html', # Nombre de template ajustado (antes recuperar_contraseña_confirmar.html)
             success_url='/recuperar-contraseña/completado/'
         ),
         name='password_reset_confirm'),
    
    path('recuperar-contraseña/completado/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='AppCitasMedicas/recuperar_contraseña_completado.html'
         ),
         name='password_reset_complete'),
]