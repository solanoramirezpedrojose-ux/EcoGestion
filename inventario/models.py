from django.db import models

class Material(models.Model):
    CATEGORIAS = [
        ('PLASTICO','Plastico'),
        ('CARTON','Carton'),
        ('PAPEL','Papel'),
        ('METAL','Metal'),
        ('VIDRIO','Vidrio'),
    ]
    nombre = models.CharField(max_length = 100, unique = True)
    categoria = models.CharField(
        max_length = 10, 
        choices = CATEGORIAS,
        default = 'PLASTICO'
    )
    precio_venta_kg = models.DecimalField(max_digits = 10, decimal_places = 2)
    stock_kg = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    activo = models.BooleanField(default = True)

    def __str__(self):
        return self.nombre