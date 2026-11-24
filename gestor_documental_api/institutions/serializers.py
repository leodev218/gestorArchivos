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


class TechnicalProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = TechnicalProgram
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)

        institution = attrs.get(
            "institution",
            self.instance.institution if self.instance else None
        )

        name = attrs.get(
            "name",
            self.instance.name if self.instance else None
        )

        # Solo las instituciones ETDH pueden tener programas técnicos.
        if institution and institution.institution_type != "ETDH":
            raise serializers.ValidationError({
                "institution": (
                    "No se pueden asociar programas técnicos a una "
                    "institución CLEI. Selecciona una institución ETDH."
                )
            })

        # El nombre solo debe ser único dentro de la misma institución.
        if institution and name:
            queryset = TechnicalProgram.objects.filter(
                institution=institution,
                name__iexact=name.strip()
            )

            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.exists():
                raise serializers.ValidationError({
                    "name": (
                        "Esta institución ya tiene registrado un programa "
                        "con ese nombre."
                    )
                })

        return attrs

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "El nombre del programa es obligatorio."
            )

        return value

    def validate_code(self, value):
        return value.strip()


class InstitutionSerializer(serializers.ModelSerializer):

    schedules = ListMultipleChoiceField(
        choices=Institution.SCHEDULE_CHOICES,
        required=False
    )

    educational_cycles = ListMultipleChoiceField(
        choices=Institution.CYCLE_CHOICES,
        required=False
    )

    # Los programas se muestran asociados a la institución,
    # pero se administran desde el módulo de programas.
    programs = TechnicalProgramSerializer(
        many=True,
        read_only=True
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

        # ETDH: no utiliza ciclos educativos CLEI.
        if institution_type == "ETDH":
            attrs["educational_cycles"] = []

        # CLEI: no puede tener programas técnicos asociados.
        elif institution_type == "CLEI":
            if self.instance and self.instance.programs.exists():
                raise serializers.ValidationError({
                    "institution_type": (
                        "Esta institución tiene programas técnicos asociados. "
                        "Debes retirarlos antes de cambiar su tipo a CLEI."
                    )
                })

        return attrs