from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import disponibilidad, CitaMedica
from .serializers import DisponibilidadSerializer, CitaMedicaSerializer
from .services.availability_service import AvailabilityService

class DisponibilidadViewSet(viewsets.ModelViewSet):
    queryset = disponibilidad.objects.all()
    serializer_class = DisponibilidadSerializer

    def create(self, request, *args, **kwargs):
        # Usamos nuestro Service para validar antes de crear vía API
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            new_disp = AvailabilityService.validate_and_create(
                medico=serializer.validated_data['medico'],
                fecha=serializer.validated_data['fecha'],
                hora_inicio=serializer.validated_data['hora_inicio'],
                hora_fin=serializer.validated_data['hora_fin']
            )
            
            response_data = DisponibilidadSerializer(new_disp).data
            headers = self.get_success_headers(response_data)
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CitaMedicaViewSet(viewsets.ModelViewSet):
    queryset = CitaMedica.objects.all()
    serializer_class = CitaMedicaSerializer
