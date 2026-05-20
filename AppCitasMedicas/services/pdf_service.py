from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from ..models import CitaMedica
import logging

logger = logging.getLogger(__name__)

class PDFService:
    @staticmethod
    def generar_comprobante_cita(cita_id):
        """
        Genera un comprobante de cita en formato PDF.
        Retorna la respuesta HTTP lista para ser enviada o un mensaje de error.
        """
        try:
            cita = CitaMedica.objects.select_related('paciente', 'medico__user').get(id_cita=cita_id)
        except CitaMedica.DoesNotExist:
            return HttpResponse("Cita no encontrada", status=404)

        template_path = 'AppCitasMedicas/pdf_confirmacion.html'
        context = {'cita': cita}
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="confirmacion_cita_{cita.paciente.cedula}.pdf"'
        
        try:
            template = get_template(template_path)
            html = template.render(context)
            pisa_status = pisa.CreatePDF(html, dest=response)
            
            if pisa_status.err:
                logger.error(f"Error al generar el PDF para cita {cita_id}")
                return HttpResponse('Error al generar el PDF', status=500)
                
            return response
        except Exception as e:
            logger.error(f"Excepción inesperada al crear PDF: {str(e)}")
            return HttpResponse('Error interno al procesar el PDF', status=500)
