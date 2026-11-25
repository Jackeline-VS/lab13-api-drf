import django_filters

from .models import Producto


class ProductoFilter(django_filters.FilterSet):
    """Filtros por query params: ?estado=activo&precio_min=500&precio_max=2000"""
    precio_min = django_filters.NumberFilter(field_name='precio', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio', lookup_expr='lte')
    categoria_nombre = django_filters.CharFilter(
        field_name='categoria__nombre', lookup_expr='icontains'
    )

    class Meta:
        model = Producto
        fields = ['estado', 'categoria']