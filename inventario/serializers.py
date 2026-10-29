from rest_framework import serializers
from.models import Material

class MaterialSerializers(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'
        # El stock es de solo lectura en la API.
        # No se puede cambiar directamente al registrar o modificar un material.
        read_only_fields = ['stock_kg']

# El stock es de solo lectura en la API.
# No se puede cambiar directamente al registrar o modificar un material.
    def validate_precio_venta_kg(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio de venta debe ser mayor a cero")
        return value
# Comprueba que el stock no sea negativo.
# Este campo tambien esta protegido como solo lectura en el serializer.
    def validate_stock_kg(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return value