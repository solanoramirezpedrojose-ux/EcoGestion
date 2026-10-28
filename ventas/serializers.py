from rest_framework import serializers
from .models import Venta, DetalleVenta

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'
        read_only_fields = ['total','estado']

    def validate_comprador(self, value):
        if not value.activo:
            raise serializers.ValidationError("El comprador debe estar activo")
        if value.tipo_persona not in ['COMPRADOR','AMBOS']:
            raise serializers.ValidationError("La persona debe ser comprador")
        return value

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = '__all__'
        read_only_fields = ['subtotal']

    def validate_cantidad_kg(self, value):
        if value <= 0:
            raise serializers.ValidationError("La canidad debe ser mayor a cero")
        return value

    def validate_precio_unitario(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a cero")
        return value

    def validate_material(self, value):
        if not value.activo:
            raise serializers.ValidationError("El material debe estar activo")
        return value

    def validate(self, data):
        venta = data.get('venta', self.instance.venta if self.instance else None)

        if self.instance and self.instance.venta.estado != 'PENDIENTE':
            raise serializers.ValidationError("No se pueden modificar detalles de una venta finalizada")

        if venta and venta.estado !='PENDIENTE':
            raise serializers.ValidationError("Solo se pueden agregar detalles a ventas pendientes")

        if self.instance and venta != self.instance.venta:
            raise serializers.ValidationError("No se puede cambiar la vente de un detalle")
        return data