
from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from .models import Institution, TechnicalProgram


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

    class Meta:
        model = Institution
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        institution_type = cleaned_data.get("institution_type")

        if institution_type == "ETDH":
            cleaned_data["educational_cycles"] = []

        return cleaned_data


class TechnicalProgramInlineFormSet(BaseInlineFormSet):

    def clean(self):
        super().clean()

        if self.instance.institution_type != "ETDH":
            for form in self.forms:
                if not hasattr(form, "cleaned_data"):
                    continue

                if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                    if form.cleaned_data.get("name"):
                        raise ValidationError(
                            "Solamente las instituciones ETDH pueden registrar programas técnicos."
                        )


class TechnicalProgramInline(admin.TabularInline):

    model = TechnicalProgram
    formset = TechnicalProgramInlineFormSet

    extra = 1
    fields = (
        "name",
        "code",
        "resolution_number",
        "resolution_date",
        "education_secretariat",
        "description",
        "is_active",
    )

    show_change_link = True

class TechnicalProgramAdminForm(forms.ModelForm):

    class Meta:
        model = TechnicalProgram
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Mostrar únicamente instituciones ETDH
        self.fields["institution"].queryset = Institution.objects.filter(
            institution_type="ETDH"
        )

    def clean(self):
        cleaned_data = super().clean()

        institution = cleaned_data.get("institution")
        name = cleaned_data.get("name")

        if institution and institution.institution_type != "ETDH":
            raise ValidationError(
                "Solo se pueden asociar programas técnicos a instituciones ETDH."
            )

        if institution and name:
            queryset = TechnicalProgram.objects.filter(
                institution=institution,
                name__iexact=name.strip()
            )

            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.exists():
                raise ValidationError(
                    "Esta institución ya tiene registrado un programa con ese nombre."
                )

        return cleaned_data
@admin.register(TechnicalProgram)
class TechnicalProgramAdmin(admin.ModelAdmin):
    form = TechnicalProgramAdminForm

    list_display = (
        "name", "institution", "resolution_number",
        "resolution_date", "is_active",
    )
    list_filter = ("institution", "is_active", "education_secretariat")
    search_fields = (
        "name", "code", "resolution_number", "institution__name",
    )
    readonly_fields = ("created_at", "updated_at")
    ordering = ("institution__name", "name")


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):

    form = InstitutionAdminForm

    list_display = (
        "name",
        "institution_type",
        "city",
        "department",
        "is_active",
    )

    list_filter = (
        "institution_type",
        "department",
        "city",
        "is_active",
    )

    search_fields = (
        "name",
        "short_name",
        "nit",
        "dane_code",
        "city",
        "department",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = [TechnicalProgramInline]

    fieldsets = (
        ("Información general", {
            "fields": (
                "name",
                "short_name",
                "institution_type",
                "is_active",
            )
        }),

        ("Ubicación y contacto", {
            "fields": (
                "country",
                "department",
                "city",
                "locality",
                "address",
                "email",
                "phone",
                "website",
                "dane_code",
                "nit",
            )
        }),

        ("Información legal", {
            "fields": (
                "operating_license",
                "resolution_number",
                "resolution_date",
                "education_secretariat",
                "legal_representative",
            )
        }),

        ("Información académica", {
            "fields": (
                "rector_name",
                "modality",
                "schedules",
                "educational_cycles",
            )
        }),

        ("Observaciones", {
            "fields": (
                "observations",
            )
        }),

        ("Auditoría", {
            "fields": (
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )

    class Media:
        js = ("institutions/js/institution_form.js",)

    def get_inlines(self, request, obj):
        if obj is not None and obj.institution_type != "ETDH":
            return []
        return super().get_inlines(request, obj)
