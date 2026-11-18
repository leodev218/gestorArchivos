from rest_framework.viewsets import ModelViewSet
from .models import DocumentCategory, DocumentTemplate
from .serializers import DocumentCategorySerializer, DocumentTemplateSerializer
class DocumentCategoryViewSet(ModelViewSet):
    queryset = DocumentCategory.objects.all()
    serializer_class = DocumentCategorySerializer
class DocumentTemplateViewSet(ModelViewSet):
    queryset = DocumentTemplate.objects.select_related('category').all()
    serializer_class = DocumentTemplateSerializer
    search_fields = ['name', 'code']
    filterset_fields = ['category', 'is_active']
