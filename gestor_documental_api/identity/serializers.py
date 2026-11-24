from rest_framework import serializers

from .models import InstitutionalIdentity
from institutions.models import Institution


class InstitutionalIdentitySerializer(serializers.ModelSerializer):

    institution_name = serializers.CharField(
        source="institution.name",
        read_only=True
    )

    class Meta:
        model = InstitutionalIdentity
        fields = "__all__"

        read_only_fields = [
            "id",
            "updated_at",
        ]

    def validate_institution(self, value):

        if self.instance:
            queryset = InstitutionalIdentity.objects.filter(
                institution=value
            ).exclude(pk=self.instance.pk)
        else:
            queryset = InstitutionalIdentity.objects.filter(
                institution=value
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "Esta institución ya tiene una identidad institucional registrada."
            )

        return value

    def validate_brand_primary_color(self, value):
        return self.validate_color(value)

    def validate_brand_secondary_color(self, value):
        return self.validate_color(value)

    def validate_color(self, value):
        if value:
            import re

            if not re.fullmatch(r"#(?:[0-9A-Fa-f]{3}){1,2}", value):
                raise serializers.ValidationError(
                    "Ingresa un color hexadecimal válido. Ejemplo: #1A73E8."
                )

        return value