from django.conf import settings
from django.db import models

class DocumentCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Categoría documental"
        verbose_name_plural = "Categorías documentales"
        ordering = ["name"]

    def __str__(self):
        return self.name

class DocumentTemplate(models.Model):
    name = models.CharField(max_length=180)
    code = models.CharField(max_length=60, unique=True)
    category = models.ForeignKey(DocumentCategory, on_delete=models.PROTECT, related_name="templates")
    file = models.FileField(upload_to="templates/source/")
    version = models.CharField(max_length=30, default="1.0")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category__name", "name"]

    def __str__(self):
        return f"{self.code} - {self.name}"
