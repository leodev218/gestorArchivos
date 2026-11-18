from rest_framework.viewsets import ModelViewSet
from .models import GeneratedDocument
from .serializers import GeneratedDocumentSerializer
class GeneratedDocumentViewSet(ModelViewSet):
    queryset = GeneratedDocument.objects.select_related('institution', 'template').all()
    serializer_class = GeneratedDocumentSerializer
    search_fields = ['title', 'consecutive', 'institution__name']
    filterset_fields = ['institution', 'template', 'status']
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
