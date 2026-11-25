from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoriaViewSet, ProductoViewSet

# El Router genera las rutas automáticamente (DRY)
router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]