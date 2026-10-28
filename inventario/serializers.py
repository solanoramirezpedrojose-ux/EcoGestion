from rest_framework import serializers
from.models import Material

class MaterialSerializers(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'
        read_only_fields = ['stock_kg']

    def validate_precio_venta_kg(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio de venta debe ser mayor a cero")
        return

    def validate_stock_kg(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return