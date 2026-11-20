
from rest_framework import serializers

from .models import Institution, TechnicalProgram


class ListMultipleChoiceField(serializers.MultipleChoiceField):
    """
    Permite mostrar opciones múltiples en el formulario HTML
    de Django REST Framework y guardar los valores como listas.
    """

    def to_internal_value(self, data):
        values = super().to_internal_value(data)
        return list(values)


class InstitutionSerializer(serializers.ModelSerializer):

    schedules = ListMultipleChoiceField(
        choices=Institution.SCHEDULE_CHOICES,
        required=False
    )

    educational_cycles = ListMultipleChoiceField(
        choices=Institution.CYCLE_CHOICES,
        required=False
    )

    programs = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=TechnicalProgram.objects.filter(is_active=True),
        required=False
    )

    class Meta:
        model = Institution
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "El nombre de la institución es obligatorio."
            )

        return value

    def validate_nit(self, value):
        value = value.strip()

        if value:
            queryset = Institution.objects.filter(nit=value)

            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.exists():
                raise serializers.ValidationError(
                    "Ya existe una institución registrada con este NIT."
                )

        return value

    def validate_dane_code(self, value):
        value = value.strip()

        if value:
            queryset = Institution.objects.filter(
                dane_code=value
            )

            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.exists():
                raise serializers.ValidationError(
                    "Ya existe una institución registrada con este código DANE."
                )

        return value

    def validate(self, attrs):

        attrs = super().validate(attrs)

        institution_type = attrs.get(
            "institution_type",
            getattr(self.instance, "institution_type", None)
        )

        # ETDH: no utiliza ciclos CLEI.
        if institution_type == "ETDH":
            attrs["educational_cycles"] = []
            return attrs

        # CLEI: no utiliza programas ETDH.
        if institution_type == "CLEI":
            attrs["programs"] = []
            return attrs

        # Otros tipos: no utilizan ciclos CLEI ni programas ETDH.
        attrs["educational_cycles"] = []
        attrs["programs"] = []

        return attrs

class TechnicalProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = TechnicalProgram
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "El nombre del programa es obligatorio."
            )

        queryset = TechnicalProgram.objects.filter(
            name__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "Ya existe un programa registrado con este nombre."
            )

        return value

    def validate_code(self, value):
        return value.strip()