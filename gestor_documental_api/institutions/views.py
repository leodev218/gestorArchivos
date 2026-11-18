from rest_framework.viewsets import ModelViewSet
from .models import Institution
from .serializers import InstitutionSerializer

class InstitutionViewSet(ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    search_fields = ['name', 'dane_code', 'nit', 'city']
    filterset_fields = ['is_active', 'department', 'city']
