from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import InstitutionalIdentity
from .serializers import InstitutionalIdentitySerializer


class InstitutionalIdentityViewSet(ModelViewSet):

    queryset = InstitutionalIdentity.objects.select_related(
        "institution"
    ).all()

    serializer_class = InstitutionalIdentitySerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "institution",
    ]

    search_fields = [
        "institution__name",
        "institution__nit",
        "institution__dane_code",
    ]

    ordering_fields = [
        "updated_at",
        "institution__name",
    ]

    ordering = ["institution__name"]