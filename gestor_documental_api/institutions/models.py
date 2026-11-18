
from django.db import models
from django.db.models import Q


class TechnicalProgram(models.Model):

    name = models.CharField(
        "Nombre del programa",
        max_length=200,
        unique=True
    )

    code = models.CharField(
        "Código del programa",
        max_length=50,
        blank=True
    )

    description = models.TextField(
        "Descripción",
        blank=True
    )

    is_active = models.BooleanField(
        "Programa activo",
        default=True
    )

    created_at = models.DateTimeField(
        "Fecha de creación",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        "Última actualización",
        auto_now=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Programa ETDH"
        verbose_name_plural = "Catálogo de programas ETDH"

    def __str__(self):
        return self.name


class Institution(models.Model):

    INSTITUTION_TYPES = [
        ("ETDH", "Educación para el Trabajo y Desarrollo Humano"),
        ("CLEI", "Educación para Jóvenes y Adultos - CLEI"),
        ("FORMAL", "Educación formal"),
        ("OTRA", "Otra"),
    ]

    SCHEDULE_CHOICES = [
        ("DIURNA", "Diurna"),
        ("NOCTURNA", "Nocturna"),
        ("SABATINA", "Sabatina"),
        ("DOMINICAL", "Dominical"),
    ]

    CYCLE_CHOICES = [
        ("CICLO_I", "Ciclo I"),
        ("CICLO_II", "Ciclo II"),
        ("CICLO_III", "Ciclo III"),
        ("CICLO_IV", "Ciclo IV"),
        ("CICLO_V", "Ciclo V"),
        ("CICLO_VI", "Ciclo VI"),
    ]

    name = models.CharField(
        "Nombre oficial",
        max_length=250
    )

    short_name = models.CharField(
        "Nombre corto",
        max_length=120,
        blank=True
    )

    institution_type = models.CharField(
        "Tipo de institución",
        max_length=20,
        choices=INSTITUTION_TYPES,
        default="OTRA"
    )

    dane_code = models.CharField(
        "Código DANE",
        max_length=30,
        blank=True
    )

    nit = models.CharField(
        "NIT",
        max_length=30,
        blank=True
    )

    country = models.CharField(
        "País",
        max_length=80,
        default="Colombia"
    )

    department = models.CharField(
        "Departamento",
        max_length=100,
        blank=True
    )

    city = models.CharField(
        "Ciudad o municipio",
        max_length=100,
        blank=True
    )

    locality = models.CharField(
        "Localidad",
        max_length=100,
        blank=True
    )

    address = models.CharField(
        "Dirección",
        max_length=250,
        blank=True
    )

    email = models.EmailField(
        "Correo electrónico",
        blank=True
    )

    phone = models.CharField(
        "Teléfono",
        max_length=50,
        blank=True
    )

    website = models.URLField(
        "Página web",
        blank=True,
        default=""
    )

    # Información legal

    operating_license = models.CharField(
        "Licencia de funcionamiento",
        max_length=250,
        blank=True
    )

    resolution_number = models.CharField(
        "Número de resolución",
        max_length=100,
        blank=True
    )

    resolution_date = models.DateField(
        "Fecha de resolución",
        null=True,
        blank=True
    )

    education_secretariat = models.CharField(
        "Secretaría de Educación",
        max_length=180,
        blank=True
    )

    legal_representative = models.CharField(
        "Representante legal",
        max_length=180,
        blank=True
    )

    # Información académica

    rector_name = models.CharField(
        "Rector(a)",
        max_length=180,
        blank=True
    )

    modality = models.CharField(
        "Modalidad educativa",
        max_length=120,
        blank=True
    )

    schedules = models.JSONField(
        "Jornadas",
        default=list,
        blank=True
    )

    educational_cycles = models.JSONField(
        "Ciclos educativos",
        default=list,
        blank=True
    )

    programs = models.ManyToManyField(
        TechnicalProgram,
        verbose_name="Programas académicos",
        blank=True,
        related_name="institutions"
    )

    observations = models.TextField(
        "Observaciones",
        blank=True
    )

    # Estado y auditoría básica

    is_active = models.BooleanField(
        "Institución activa",
        default=True
    )

    created_at = models.DateTimeField(
        "Fecha de creación",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        "Última actualización",
        auto_now=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Institución"
        verbose_name_plural = "Instituciones"

        constraints = [
            models.UniqueConstraint(
                fields=["nit"],
                condition=~Q(nit=""),
                name="unique_institution_nit_nonempty"
            ),
            models.UniqueConstraint(
                fields=["dane_code"],
                condition=~Q(dane_code=""),
                name="unique_institution_dane_nonempty"
            ),
        ]

        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["department", "city"]),
            models.Index(fields=["institution_type"]),
        ]

    def __str__(self):
        return self.name
