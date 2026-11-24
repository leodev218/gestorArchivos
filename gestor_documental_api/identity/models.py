from django.db import models
from django.core.validators import RegexValidator
from institutions.models import Institution


hex_color_validator = RegexValidator(
    regex=r"^#(?:[0-9A-Fa-f]{3}){1,2}$",
    message="Ingresa un color hexadecimal válido. Ejemplo: #1A73E8."
)


class InstitutionalIdentity(models.Model):

    institution = models.OneToOneField(
        Institution,
        on_delete=models.CASCADE,
        related_name="identity",
        verbose_name="Institución"
    )

    logo = models.ImageField(
        "Logotipo institucional",
        upload_to="institutions/logos/",
        blank=True,
        null=True
    )

    letterhead = models.FileField(
        "Membrete institucional",
        upload_to="institutions/letterheads/",
        blank=True,
        null=True
    )

    authorized_signature = models.ImageField(
        "Firma autorizada",
        upload_to="institutions/signatures/",
        blank=True,
        null=True
    )

    footer_text = models.TextField(
        "Texto del pie de página",
        blank=True
    )

    brand_primary_color = models.CharField(
        "Color institucional principal",
        max_length=7,
        blank=True,
        validators=[hex_color_validator]
    )

    brand_secondary_color = models.CharField(
        "Color institucional secundario",
        max_length=7,
        blank=True,
        validators=[hex_color_validator]
    )

    notes = models.TextField(
        "Observaciones",
        blank=True
    )

    updated_at = models.DateTimeField(
        "Última actualización",
        auto_now=True
    )

    class Meta:
        ordering = ["institution__name"]
        verbose_name = "Identidad institucional"
        verbose_name_plural = "Identidades institucionales"

    def __str__(self):
        return f"Identidad: {self.institution.name}"