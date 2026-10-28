from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from personas.models import Persona
from inventario.models import Material
from .models import Venta, DetalleVenta

class VentaTest(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_superuser(
            username='admin_prueba',
            password='12345678'
        )
        token = Token.objects.create(user=self.usuario)
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + token.key
        )
        self.comprador = Persona.objects.create(
            nombre='Maria Lopez',
            identificacion='987654321',
            telefono='88887777',
            correo='maria@gmail.com',
            direccion='Esparza',
            tipo_persona='COMPRADOR'
        )
        self.material = Material.objects.create(
            nombre='Aluminio',
            categoria='METAL',
            precio_venta_kg=500,
            stock_kg=50
        )
        self.venta = Venta.objects.create(
            comprador=self.comprador
        )
        self.detalle = DetalleVenta.objects.create(
            venta=self.venta,
            material=self.material,
            cantidad_kg=10,
            precio_unitario=500,
            subtotal=5000
        )

    # PRUEBA 1: CONFIRMAR VENTA
    def test_confirmar_venta(self):
        respuesta = self.client.post(
            '/api/ventas/' + str(self.venta.id) + '/confirmar/'
        )
        self.assertEqual(respuesta.status_code, 200)
        self.material.refresh_from_db()
        self.venta.refresh_from_db()
        self.assertEqual(self.material.stock_kg, 40)
        self.assertEqual(self.venta.estado, 'CONFIRMADA')
        self.assertEqual(self.venta.total, 5000)

    # PRUEBA 2: STOCK INSUFICIENTE
    def test_stock_insuficiente(self):
        self.material.stock_kg = 5
        self.material.save()
        respuesta = self.client.post(
            '/api/ventas/' + str(self.venta.id) + '/confirmar/'
        )
        self.assertEqual(respuesta.status_code, 409)
        self.material.refresh_from_db()
        self.venta.refresh_from_db()
        self.assertEqual(self.material.stock_kg, 5)
        self.assertEqual(self.venta.estado, 'PENDIENTE')