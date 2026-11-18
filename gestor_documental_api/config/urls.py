from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from core.views import health
from institutions.views import InstitutionViewSet
from identity.views import InstitutionalIdentityViewSet
from templates_manager.views import DocumentCategoryViewSet, DocumentTemplateViewSet
from documents.views import GeneratedDocumentViewSet

router = DefaultRouter()
router.register("institutions", InstitutionViewSet)
router.register("identities", InstitutionalIdentityViewSet)
router.register("categories", DocumentCategoryViewSet)
router.register("templates", DocumentTemplateViewSet)
router.register("generated-documents", GeneratedDocumentViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health, name="health"),
    path("api/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
