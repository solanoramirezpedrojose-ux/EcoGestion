from django.db import models
from django.utils import timezone
from personas.models import Persona
from inventario.models import Material

class Venta(models.Model):
    ESTADOS = [
        ('PENDIENTE','Pendiente'),
        ('CONFIRMADA','Confirmada'),
        ('ANULADA','Anulada'),
    ]
    comprador = models.ForeignKey(
        Persona,
        on_delete = models.PROTECT,
        related_name = 'ventas'
    )
    fecha = models.DateTimeField(default = timezone.now)
    total = models.DecimalField(max_digits = 12, decimal_places = 2, default = 0)
    estado = models.CharField(
        max_length = 10,
        choices = ESTADOS,
        default = 'PENDIENTE'
    )

    def __str__(self):
        return f"Venta {self.id} - {self.comprador.nombre}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(
        Venta,
        on_delete = models.CASCADE,
        related_name = 'detalles'
    )
    material = models.ForeignKey(
        Material,
        on_delete = models.PROTECT,
        related_name = 'detalles_venta'
    )
    cantidad_kg = models.DecimalField(max_digits = 10, decimal_places = 2)
    precio_unitario = models.DecimalField(max_digits = 10, decimal_places = 2)
    subtotal = models.DecimalField(max_digits = 12, decimal_places = 2, default = 0)

    def __str__(self):
        return f"{self.material.nombre} - {self.cantidad_kg} kg"