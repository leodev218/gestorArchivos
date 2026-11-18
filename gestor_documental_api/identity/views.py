from rest_framework.viewsets import ModelViewSet
from .models import InstitutionalIdentity
from .serializers import InstitutionalIdentitySerializer
class InstitutionalIdentityViewSet(ModelViewSet):
    queryset = InstitutionalIdentity.objects.select_related('institution').all()
    serializer_class = InstitutionalIdentitySerializer
