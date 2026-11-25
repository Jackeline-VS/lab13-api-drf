from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Categoria, Producto
from .serializers import CategoriaSerializer, ProductoSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    """
    CRUD de categorías.
    GET→list/retrieve · POST→create · PUT/PATCH→update · DELETE→destroy
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    # Endpoint custom: /api/categorias/{id}/productos/
    @action(detail=True, methods=['get'])
    def productos(self, request, pk=None):
        categoria = self.get_object()
        qs = categoria.productos.select_related('categoria')
        page = self.paginate_queryset(qs)
        serializer = ProductoSerializer(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)


class ProductoViewSet(viewsets.ModelViewSet):
    """
    CRUD de productos. Permisos, paginación y throttling vienen de settings (globales).
    """
    # select_related evita N+1 consultas al traer la categoría
    queryset = Producto.objects.select_related('categoria').all()
    serializer_class = ProductoSerializer

    # Endpoint custom de colección: /api/productos/activos/
    @action(detail=False, methods=['get'])
    def activos(self, request):
        qs = self.filter_queryset(self.get_queryset().filter(estado='activo'))
        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    # Endpoint custom de detalle: POST /api/productos/{id}/desactivar/
    @action(detail=True, methods=['post'])
    def desactivar(self, request, pk=None):
        producto = self.get_object()
        producto.estado = 'inactivo'
        producto.save(update_fields=['estado', 'actualizado'])
        return Response(self.get_serializer(producto).data)