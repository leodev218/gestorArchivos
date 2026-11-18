from django.conf import settings
from django.db import models

class AuditEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=80)
    entity_type = models.CharField(max_length=100)
    entity_id = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Evento de auditoría"
        verbose_name_plural = "Eventos de auditoría"

    def __str__(self):
        return f"{self.action} - {self.entity_type} - {self.created_at:%Y-%m-%d %H:%M}"
