
from django import forms
from django.contrib import admin
from .models import Institution, TechnicalProgram


@admin.register(TechnicalProgram)
class TechnicalProgramAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "code",
        "is_active",
        "created_at",
    )

    list_filter = ("is_active",)

    search_fields = (
        "name",
        "code",
        "description",
    )

    ordering = ("name",)

    list_editable = ("is_active",)

    list_per_page = 25

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Información del programa",
            {
                "fields": (
                    "name",
                    "code",
                    "description",
                    "is_active",
                )
            }
        ),
        (
            "Control",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            }
        ),
    )


class InstitutionAdminForm(forms.ModelForm):

    schedules = forms.MultipleChoiceField(
        label="Jornadas",
        choices=Institution.SCHEDULE_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    educational_cycles = forms.MultipleChoiceField(
        label="Ciclos educativos",
        choices=Institution.CYCLE_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    programs = forms.ModelMultipleChoiceField(
        label="Programas académicos",
        queryset=TechnicalProgram.objects.filter(is_active=True),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Institution
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        institution_type = cleaned_data.get("institution_type")

        if institution_type == "CLEI":
            cleaned_data["programs"] = TechnicalProgram.objects.none()

        elif institution_type == "ETDH":
            cleaned_data["educational_cycles"] = []

        else:
            cleaned_data["educational_cycles"] = []
            cleaned_data["programs"] = TechnicalProgram.objects.none()

        return cleaned_data


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):

    form = InstitutionAdminForm

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

    filter_horizontal = ()

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    class Media:
        js = (
            "institutions/js/institution_form.js",
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
