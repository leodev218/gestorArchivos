from django.db import models
from institutions.models import Institution

class InstitutionalIdentity(models.Model):
    institution = models.OneToOneField(Institution, on_delete=models.CASCADE, related_name="identity")
    logo = models.ImageField(upload_to="institutions/logos/", blank=True, null=True)
    letterhead = models.FileField(upload_to="institutions/letterheads/", blank=True, null=True)
    authorized_signature = models.ImageField(upload_to="institutions/signatures/", blank=True, null=True)
    footer_text = models.TextField(blank=True)
    brand_primary_color = models.CharField(max_length=20, blank=True)
    brand_secondary_color = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Identidad: {self.institution.name}"
