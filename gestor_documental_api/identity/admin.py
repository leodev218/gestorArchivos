
from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import InstitutionalIdentity


class ColorInput(forms.widgets.Input):
    input_type = "color"


class ColorPickerWidget(forms.TextInput):

    def render(self, name, value, attrs=None, renderer=None):

        attrs = attrs or {}
        text_attrs = attrs.copy()

        field_id = text_attrs.get("id", f"id_{name}")

        text_attrs["class"] = (
            text_attrs.get("class", "") + " color-hex-input"
        ).strip()

        text_html = super().render(
            name,
            value,
            text_attrs,
            renderer
        )

        # Normalizar el color para el selector visual.
        valid_color = "#000000"

        if value:
            value = value.strip()

            if len(value) == 4 and value.startswith("#"):
                valid_color = (
                    "#" + "".join(char * 2 for char in value[1:])
                )
            elif len(value) == 7 and value.startswith("#"):
                valid_color = value

        color_attrs = {
            "id": f"{field_id}_picker",
            "class": "color-picker-input",
            "value": valid_color,
        }

        color_html = ColorInput().render(
            f"{name}_picker",
            valid_color,
            color_attrs,
            renderer
        )

        return format_html(
            '<div class="color-picker-container">{} {}</div>',
            color_html,
            text_html
        )


class InstitutionalIdentityAdminForm(forms.ModelForm):

    class Meta:
        model = InstitutionalIdentity
        fields = "__all__"

        widgets = {
            "brand_primary_color": ColorPickerWidget(),
            "brand_secondary_color": ColorPickerWidget(),
        }


@admin.register(InstitutionalIdentity)
class InstitutionalIdentityAdmin(admin.ModelAdmin):

    form = InstitutionalIdentityAdminForm

    list_display = (
        "institution",
        "logo_preview",
        "brand_primary_color",
        "brand_secondary_color",
        "updated_at",
    )

    search_fields = (
        "institution__name",
        "institution__nit",
        "institution__dane_code",
    )

    readonly_fields = (
        "logo_preview",
        "signature_preview",
        "updated_at",
    )

    autocomplete_fields = ("institution",)

    fieldsets = (
        ("Institución", {
            "fields": ("institution",)
        }),

        ("Imagen institucional", {
            "fields": (
                "logo",
                "logo_preview",
                "letterhead",
                "authorized_signature",
                "signature_preview",
            )
        }),

        ("Identidad visual", {
            "fields": (
                "brand_primary_color",
                "brand_secondary_color",
            )
        }),

        ("Información documental", {
            "fields": (
                "footer_text",
                "notes",
            )
        }),

        ("Auditoría", {
            "fields": ("updated_at",)
        }),
    )

    class Media:
        js = ("identity/js/color_picker.js",)
        css = {
            "all": ("identity/css/color_picker.css",)
        }

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" width="100" style="object-fit:contain;" />',
                obj.logo.url
            )
        return "Sin logotipo"

    logo_preview.short_description = "Vista previa del logotipo"

    def signature_preview(self, obj):
        if obj.authorized_signature:
            return format_html(
                '<img src="{}" width="180" style="object-fit:contain;" />',
                obj.authorized_signature.url
            )
        return "Sin firma"

    signature_preview.short_description = "Vista previa de la firma"
