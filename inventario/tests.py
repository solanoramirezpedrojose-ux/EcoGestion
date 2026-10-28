from django.test import TestCase
from .models import Material
from .serializers import MaterialSerializers

class MaterialTest(TestCase):
    #Prueba 1: No permitir precios negativos
    def test_precio_negativo(self):
        datos = {
            'nombre':'Aluminio',
            'categoria':'METAL',
            'precio_venta_kg': -100
        }
        serializer = MaterialSerializers(data = datos)
        self.assertFalse(serializer.is_valid())

    #Prueba 2: Aceptar un material Valido
    def test_material_valido(self):
        datos = {
            'nombre':'Carton',
            'categoria':'CARTON',
            'precio_venta_kg': 150
        }
        serializer = MaterialSerializers(data = datos)
        self.assertTrue(serializer.is_valid())

    #Prueba 3: Proteger el stock
    def test_stock_no_modificable(self):
        material = Material.objects.create(
            nombre='Plastico',
            categoria='PLASTICO',
            precio_venta_kg=200,
            stock_kg=50
        )
        serializer = MaterialSerializers(
            material,
            data={'stock_kg': 100},
            partial=True
        )
        self.assertTrue(serializer.is_valid())
        serializer.save()
        material.refresh_from_db()
        self.assertEqual(material.stock_kg, 50)