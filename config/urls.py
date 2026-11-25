from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('productos.urls')),
    path('api-auth/', include('rest_framework.urls')),
    # Documentación OpenAPI 3 (contrato máquina-legible)
    # IA: [warnings de spectacular por SerializerMethodField sin tipo] → Solución manual:
    # se añadieron type hints (-> int, -> Decimal, -> dict) en los métodos get_*.
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]