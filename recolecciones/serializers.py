from rest_framework import serializers
from .models import Recoleccion, DetalleRecoleccion

class RecoleccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recoleccion
        fields = '__all__'
        read_only_fields = ['estado']

    def validate_proveedor(self, value):
        if not value.activo:
            raise serializers.ValidationError("El proveedor debe ser activo")
        if value.tipo_persona not in ['PROVEEDOR','AMBOS']:
            raise serializers.ValidationError("La persona debe ser proveedor")
        return value

class DetalleRecoleccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleRecoleccion
        fields = '__all__'

    def validate_cantidad_kg(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a cero")
        return value

    def validate_material(self, value):
        if not value.activo:
            raise serializers.ValidationError("El material debe estar activo")
        return value

    def validate(self, data):
        recoleccion = data.get('recoleccion',self.instance.recoleccion if self.instance else None)
        if self.instance and self.instance.recoleccion.estado != 'PENDIENTE':
            raise serializers.ValidationError("No se puede modificiar detalles de una recoleccion finalizada")
        if recoleccion and recoleccion.estado != 'PENDIENTE':
            raise serializers.ValidationError("Solo se pueden agregar detaller a recoleccione pendientes")
        if self.instance and recoleccion != self.instance.recoleccion:
            raise serializers.ValidationError(
                "No se puede cambiar la recolección de un detalle."
            )
        return data