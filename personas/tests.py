from django.test import TestCase
from django.contrib.auth.models import User, Group, Permission
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Persona

class PersonaTest(TestCase):
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
        self.persona = Persona.objects.create(
            nombre='Juan Perez',
            identificacion='123456789',
            telefono='88887777',
            correo='juan@gmail.com',
            direccion='Puntarenas',
            tipo_persona='PROVEEDOR'
        )

    # PRUEBA 1: LISTAR PERSONAS
    def test_listar_personas(self):
        respuesta = self.client.get('/api/personas/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.data), 1)

    # PRUEBA 2: CREAR PERSONA
    def test_crear_persona(self):
        datos = {
            'nombre': 'Maria Lopez',
            'identificacion': '987654321',
            'telefono': '89998888',
            'correo': 'maria@gmail.com',
            'direccion': 'Esparza',
            'tipo_persona': 'COMPRADOR'
        }
        respuesta = self.client.post(
            '/api/personas/',
            datos,
            format='json'
        )
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(Persona.objects.count(), 2)

    # PRUEBA 3: CONSULTAR PERSONA
    def test_consultar_persona(self):
        respuesta = self.client.get(
            '/api/personas/' + str(self.persona.id) + '/'
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data['nombre'], 'Juan Perez')

    # PRUEBA 4: MODIFICAR PERSONA CON PATCH
    def test_modificar_persona(self):
        datos = {
            'telefono': '87776666'
        }
        respuesta = self.client.patch(
            '/api/personas/' + str(self.persona.id) + '/',
            datos,
            format='json'
        )
        self.assertEqual(respuesta.status_code, 200)
        self.persona.refresh_from_db()
        self.assertEqual(self.persona.telefono, '87776666')

    # PRUEBA 5: ELIMINAR PERSONA
    def test_eliminar_persona(self):
        respuesta = self.client.delete(
            '/api/personas/' + str(self.persona.id) + '/'
        )
        self.assertEqual(respuesta.status_code, 204)
        self.assertEqual(Persona.objects.count(), 0)


class PermisosPersonaTest(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username='consulta_prueba',
            password='12345678'
        )
        grupo = Group.objects.create(name='Consulta')
        permiso = Permission.objects.get(
            codename='view_persona',
            content_type__app_label='personas'
        )
        grupo.permissions.add(permiso)
        self.usuario.groups.add(grupo)
        token = Token.objects.create(user=self.usuario)
        self.cliente = APIClient()
        self.token = token.key

    # PRUEBA 1: NO PERMITIR ACCESO SIN TOKEN
    def test_sin_token(self):
        respuesta = self.cliente.get('/api/personas/')
        self.assertEqual(respuesta.status_code, 401)

    # PRUEBA 2: USUARIO CONSULTA PUEDE VER PERSONAS
    def test_consultar_personas(self):
        self.cliente.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token
        )
        respuesta = self.cliente.get('/api/personas/')
        self.assertEqual(respuesta.status_code, 200)

    # PRUEBA 3: USUARIO CONSULTA NO PUEDE CREAR
    def test_no_puede_crear(self):
        self.cliente.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token
        )
        datos = {
            'nombre': 'Carlos Lopez',
            'identificacion': '111222333',
            'telefono': '88887777',
            'correo': 'carlos@gmail.com',
            'direccion': 'Esparza',
            'tipo_persona': 'PROVEEDOR'
        }
        respuesta = self.cliente.post(
            '/api/personas/',
            datos,
            format='json'
        )
        self.assertEqual(respuesta.status_code, 403)