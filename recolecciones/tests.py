from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from personas.models import Persona
from inventario.models import Material
from .models import Recoleccion, DetalleRecoleccion
from .serializers import RecoleccionSerializer, DetalleRecoleccionSerializer

class RecoleccionTest(TestCase):
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
        self.proveedor = Persona.objects.create(
            nombre='Juan Perez',
            identificacion='123456789',
            telefono='88887777',
            correo='juan@gmail.com',
            direccion='Puntarenas',
            tipo_persona='PROVEEDOR'
        )
        self.material = Material.objects.create(
            nombre='Aluminio',
            categoria='METAL',
            precio_venta_kg=500,
            stock_kg=0
        )
        self.recoleccion = Recoleccion.objects.create(
            proveedor=self.proveedor
        )
        self.detalle = DetalleRecoleccion.objects.create(
            recoleccion=self.recoleccion,
            material=self.material,
            cantidad_kg=20
        )

    # PRUEBA 1: NO PERMITIR CANTIDADES NEGATIVAS
    def test_cantidad_negativa(self):
        datos = {
            'recoleccion': self.recoleccion.id,
            'material': self.material.id,
            'cantidad_kg': -5
        }
        serializer = DetalleRecoleccionSerializer(data=datos)
        self.assertFalse(serializer.is_valid())

    # PRUEBA 2: NO PERMITIR PROVEEDORES INACTIVOS
    def test_proveedor_inactivo(self):
        self.proveedor.activo = False
        self.proveedor.save()
        datos = {
            'proveedor': self.proveedor.id
        }
        serializer = RecoleccionSerializer(data=datos)
        self.assertFalse(serializer.is_valid())

    # PRUEBA 3: CONFIRMAR RECOLECCION
    def test_confirmar_recoleccion(self):
        respuesta = self.client.post(
            '/api/recolecciones/' + str(self.recoleccion.id) + '/confirmar/'
        )
        self.assertEqual(respuesta.status_code, 200)
        self.material.refresh_from_db()
        self.recoleccion.refresh_from_db()
        self.assertEqual(self.material.stock_kg, 20)
        self.assertEqual(self.recoleccion.estado, 'RECIBIDA')