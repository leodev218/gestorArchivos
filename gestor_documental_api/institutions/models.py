from django.db import models

class Institution(models.Model):
    name = models.CharField("Nombre oficial", max_length=250)
    short_name = models.CharField("Nombre corto", max_length=120, blank=True)
    dane_code = models.CharField("Código DANE", max_length=30, blank=True)
    nit = models.CharField(max_length=30, blank=True)
    city = models.CharField("Ciudad o municipio", max_length=100, blank=True)
    department = models.CharField("Departamento", max_length=100, blank=True)
    country = models.CharField(max_length=80, default="Colombia")
    address = models.CharField("Dirección", max_length=250, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    operating_license = models.CharField("Licencia / resolución", max_length=250, blank=True)
    education_secretariat = models.CharField("Secretaría de Educación", max_length=180, blank=True)
    legal_representative = models.CharField(max_length=180, blank=True)
    rector_name = models.CharField("Rector(a)", max_length=180, blank=True)
    modality = models.CharField(max_length=120, blank=True)
    schedules = models.JSONField(default=list, blank=True)
    educational_cycles = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Institución"
        verbose_name_plural = "Instituciones"

    def __str__(self):
        return self.name
