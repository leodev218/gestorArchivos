
from django.contrib import admin
from .models import Institution


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "institution_type",
        "nit",
        "dane_code",
        "city",
        "department",
        "is_active",
        "created_at",
    )

    list_filter = (
        "institution_type",
        "is_active",
        "department",
        "city",
    )

    search_fields = (
        "name",
        "short_name",
        "nit",
        "dane_code",
        "legal_representative",
        "rector_name",
    )

    ordering = ("name",)

    list_per_page = 25

    date_hierarchy = "created_at"

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Información general",
            {
                "fields": (
                    "name",
                    "short_name",
                    "institution_type",
                    "nit",
                    "dane_code",
                    "is_active",
                )
            }
        ),
        (
            "Ubicación y contacto",
            {
                "fields": (
                    "country",
                    "department",
                    "city",
                    "locality",
                    "address",
                    "email",
                    "phone",
                    "website",
                )
            }
        ),
        (
            "Información legal",
            {
                "fields": (
                    "education_secretariat",
                    "operating_license",
                    "resolution_number",
                    "resolution_date",
                    "legal_representative",
                )
            }
        ),
        (
            "Información académica",
            {
                "fields": (
                    "rector_name",
                    "modality",
                    "schedules",
                    "educational_levels",
                    "educational_cycles",
                    "programs",
                )
            }
        ),
        (
            "Observaciones y control",
            {
                "fields": (
                    "observations",
                    "created_at",
                    "updated_at",
                )
            }
        ),
    )
