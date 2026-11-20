
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Institution, TechnicalProgram
from .serializers import (
    InstitutionSerializer,
    TechnicalProgramSerializer,
)


class InstitutionViewSet(ModelViewSet):

    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "name",
        "short_name",
        "dane_code",
        "nit",
        "city",
        "department",
        "locality",
        "legal_representative",
        "rector_name",
    ]

    filterset_fields = [
        "is_active",
        "institution_type",
        "department",
        "city",
        "country",
    ]

    ordering_fields = [
        "name",
        "created_at",
        "updated_at",
        "city",
        "department",
    ]

    ordering = ["name"]

    @action(detail=True, methods=["post"], url_path="activar")
    def activar(self, request, pk=None):

        institution = self.get_object()
        institution.is_active = True
        institution.save()

        serializer = self.get_serializer(institution)

        return Response(
            {
                "message": "Institución activada correctamente.",
                "institution": serializer.data,
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"], url_path="desactivar")
    def desactivar(self, request, pk=None):

        institution = self.get_object()
        institution.is_active = False
        institution.save()

        serializer = self.get_serializer(institution)

        return Response(
            {
                "message": "Institución desactivada correctamente.",
                "institution": serializer.data,
            },
            status=status.HTTP_200_OK
        )


class TechnicalProgramViewSet(ModelViewSet):

    queryset = TechnicalProgram.objects.all()
    serializer_class = TechnicalProgramSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "name",
        "code",
        "description",
    ]

    filterset_fields = [
        "is_active",
    ]

    ordering_fields = [
        "name",
        "created_at",
        "updated_at",
    ]

    ordering = ["name"]

    @action(detail=True, methods=["post"], url_path="activar")
    def activar(self, request, pk=None):

        program = self.get_object()
        program.is_active = True
        program.save()

        serializer = self.get_serializer(program)

        return Response(
            {
                "message": "Programa activado correctamente.",
                "program": serializer.data,
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"], url_path="desactivar")
    def desactivar(self, request, pk=None):

        program = self.get_object()
        program.is_active = False
        program.save()

        serializer = self.get_serializer(program)

        return Response(
            {
                "message": "Programa desactivado correctamente.",
                "program": serializer.data,
            },
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):

        program = self.get_object()

        if program.institutions.exists():
            return Response(
                {
                    "message": (
                        "No se puede eliminar este programa porque "
                        "está asignado a una o varias instituciones. "
                        "Puedes desactivarlo en su lugar."
                    )
                },
                status=status.HTTP_409_CONFLICT
            )

        return super().destroy(request, *args, **kwargs)
