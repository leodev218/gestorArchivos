
from rest_framework import serializers
from .models import Institution


class InstitutionSerializer(serializers.ModelSerializer):

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

    def validate_schedules(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError(
                "Las jornadas deben enviarse como una lista."
            )

        return value

    def validate_educational_levels(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError(
                "Los niveles educativos deben enviarse como una lista."
            )

        return value

    def validate_educational_cycles(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError(
                "Los ciclos educativos deben enviarse como una lista."
            )

        return value

    def validate_programs(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError(
                "Los programas deben enviarse como una lista."
            )

        return value
