from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('productos.urls')),
    # Login/logout de la API navegable (autenticación por sesión)
    path('api-auth/', include('rest_framework.urls')),
]