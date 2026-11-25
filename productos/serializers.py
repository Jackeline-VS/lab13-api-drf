from decimal import Decimal

from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Categoria, Producto


class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    # Campo calculado (solo lectura)
    total_productos = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = ('id', 'url', 'nombre', 'descripcion', 'total_productos', 'creado')
        read_only_fields = ('creado',)

    def get_total_productos(self, obj):
        return obj.productos.count()


class ProductoSerializer(serializers.HyperlinkedModelSerializer):
    # Relación hipervinculada (HATEOAS): devuelve la URL de la categoría
    categoria = serializers.HyperlinkedRelatedField(
        view_name='categoria-detail',
        queryset=Categoria.objects.all(),
    )
    # Campo de solo lectura tomado de la relación
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    # Campos calculados
    precio_con_igv = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        # Lista explícita de campos: no se expone nada sensible
        fields = (
            'id', 'url', 'nombre', 'descripcion', 'precio', 'precio_con_igv',
            'stock', 'estado', 'categoria', 'categoria_nombre',
            'creado', 'actualizado', 'links',
        )
        read_only_fields = ('creado', 'actualizado')

    def get_precio_con_igv(self, obj):
        return round(obj.precio * Decimal('1.18'), 2)

    def get_links(self, obj):
        """HATEOAS básico: enlaces de navegación para el cliente."""
        request = self.context.get('request')
        return {
            'self': reverse('producto-detail', args=[obj.pk], request=request),
            'categoria': reverse('categoria-detail', args=[obj.categoria_id], request=request),
            'coleccion': reverse('producto-list', request=request),
        }

    # --- Validaciones (en el serializador, no en la vista) ---
    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError('El precio debe ser mayor que 0.')
        return value

    def validate_nombre(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError('El nombre debe tener al menos 3 caracteres.')
        return value.strip()

    def validate(self, data):
        """Validación cruzada: un producto activo no puede tener stock 0."""
        estado = data.get('estado', getattr(self.instance, 'estado', 'activo'))
        stock = data.get('stock', getattr(self.instance, 'stock', 0))
        if estado == 'activo' and stock == 0:
            raise serializers.ValidationError(
                {'stock': 'Un producto activo debe tener stock mayor a 0.'}
            )
        return data