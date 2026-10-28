from django.db import models

class Persona(models.Model):
    TIPOS_PERSONA = [
        ('PROVEEDOR','Proveedor'),
        ('COMPRADOR','Comprador'),
        ('AMBOS','Ambos')
    ]
    nombre = models.CharField(max_length = 100)
    identificacion = models.CharField(max_length = 30, unique = True)
    telefono = models.CharField(max_length = 20)
    correo = models.EmailField()
    direccion = models.CharField(max_length = 200)
    tipo_persona = models.CharField(
        max_length = 10,
        choices = TIPOS_PERSONA,
        default = 'PROVEEDOR'
    )
    activo = models.BooleanField(default = True)
    fecha_registro = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.nombre