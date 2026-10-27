from django.db import models
from django.utils import timezone
from personas.models import Persona
from inventario.models import Material

class Recoleccion(models.Model):
    ESTADOS = [
        ('PENDIENTE','Pendiente'),
        ('RECIBIDA','Recibida'),
        ('CANCELADA','Cancelada')
    ]
    proveedor = models.ForeignKey(
        Persona,
        on_delete = models.PROTECT,
        related_name = 'recolecciones'
    )
    fecha = models.DateTimeField(default = timezone.now)
    estado = models.CharField(
        max_length = 10,
        choices = ESTADOS,
        default = 'PENDIENTE'
    )
    observaciones = models.TextField(blank = True)

    def __str__(self):
        return f"Recoleccion {self.id} - {self.proveedor.nombre}"

class DetalleRecoleccion(models.Model):
    recoleccion = models.ForeignKey(
        Recoleccion,
        on_delete = models.CASCADE,
        related_name = 'detalles'
    )
    material = models.ForeignKey(
        Material,
        on_delete = models.PROTECT,
        related_name = 'detalles_recoleccion'
    )
    cantidad_kg = models.DecimalField(max_digits = 10, decimal_places = 2)

    def __str__(self):
        return f"{self.material.nombre} - {self.cantidad_kg} kg"