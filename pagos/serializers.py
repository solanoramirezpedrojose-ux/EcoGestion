from rest_framework import serializers
from django.db.models import Sum
from decimal import Decimal
from .models import Pago

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

    def validate_monto(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto del pago debe ser mayor a cero")
        return value

    def validate(self, data):
        venta = data.get('venta', self.instance.venta if self.instance else None)
        monto = data.get('monto', self.instance.monto if self.instance else None)
        if self.instance and venta != self.instance.venta:
            raise serializers.ValidationError("No se puede cambiar la venta de un pago")
        if venta.estado != 'CONFIRMADA':
            raise serializers.ValidationError("Solo se pueden tegistrar pagos de ventas confirmadas")
        pagos = Pago.objects.filter(venta=venta)
        if self.instance:
            pagos = pagos.exclude(pk=self.instance.pk)
        total_pagado = pagos.aggregate(
            total = Sum('monto')
        )['total'] or Decimal('0.00')

        if total_pagado + monto > venta.total:
            raise serializers.ValidationError("El pago supera el saldo pendiente de la venta")
        return data