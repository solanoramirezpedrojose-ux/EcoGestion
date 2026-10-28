from django.db import models
from django.utils import timezone
from ventas.models import Venta

class Pago(models.Model):
    METODOS_PAGO = [
        ('EFECTIVO','Efectivo'),
        ('TRANSFERENCIA','Transferencia'),
        ('SINPE','Sinpe Movil')
    ]
    venta = models.ForeignKey(
        Venta,
        on_delete = models.PROTECT,
        related_name = 'pagos'
    )
    monto = models.DecimalField(max_digits = 12, decimal_places = 2)
    metodo_pago = models.CharField(
        max_length = 15,
        choices = METODOS_PAGO,
        default = 'EFECTIVO',
    )
    referencia = models.CharField(max_length = 100, blank = True)
    fecha_pago = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Pago {self.id} - Venta {self.venta.id}"