from django.conf import settings
from django.db import models
from institutions.models import Institution
from templates_manager.models import DocumentTemplate

class GeneratedDocument(models.Model):
    STATUS_CHOICES = [("draft", "Borrador"), ("generated", "Generado"), ("error", "Error")]
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT, related_name="documents")
    template = models.ForeignKey(DocumentTemplate, on_delete=models.PROTECT, related_name="generated_documents")
    title = models.CharField(max_length=250)
    output_file = models.FileField(upload_to="documents/generated/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    consecutive = models.CharField(max_length=60, blank=True)
    data_snapshot = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
