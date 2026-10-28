# EcoGestión

Sistema de gestión para un centro de acopio y reciclaje, desarrollado con Django y Django REST Framework.
## Descripción del proyecto
EcoGestión es una API REST que permite administrar las operaciones de un centro de acopio, incluyendo el registro de personas, el control de materiales reciclables, las recolecciones, las ventas y los pagos.

El sistema permite gestionar el inventario de materiales y controlar el acceso mediante autenticación por tokens y permisos de usuario.

## Tecnologías utilizadas
- Python
- Django 5.2
- Django REST Framework
- MySQL
- TokenAuthentication
- Postman
- Git y GitHub

## Módulos del sistema
1. Personas: administración de proveedores y compradores.
2. Inventario: registro de materiales, precios y existencias.
3. Recolecciones: registro de materiales recibidos y actualización del inventario.
4. Ventas: registro de ventas y descuento de materiales del inventario.
5. Pagos: registro de pagos asociados a las ventas.

## Diagrama entidad-relación

El siguiente diagrama representa los siete modelos del sistema EcoGestión, sus atributos, claves primarias, claves foráneas y relaciones.

![Diagrama entidad-relación de EcoGestión](docs/DiagramaEntidad-Relacion.jpg)

## Requisitos previos
- Tener Python instalado.
- Tener MySQL instalado y funcionando.
- Tener acceso a una terminal.
- Contar con las credenciales de un usuario MySQL con permisos sobre la base de datos.

## Instalación del proyecto
1. Obtener el proyecto
Clonar el repositorio desde GitHub y abrir la carpeta EcoGestion en Visual Studio Code.

### 2. Crear el entorno virtual
Desde la carpeta donde se encuentra manage.py, ejecutar:
    py -m venv .venv
Activar el entorno virtual en PowerShell:
    .\.venv\Scripts\Activate.ps1

### 3. Instalar las dependencias
Ejecutar:
    pip install -r requirements.txt

### 4. Configurar la base de datos
Crear una base de datos en MySQL llamada:
    ecogestion_db
El usuario de MySQL debe tener permisos sobre esta base de datos.

### 5. Configurar las variables de entorno
Copiar el archivo .env.example y renombrar la copia como .env.
Completar las variables con las credenciales correspondientes:
    DB_NAME=ecogestion_db
    DB_USER=tu_usuario_mysql
    DB_PASSWORD=tu_contrasena_mysql
    DB_HOST=localhost
    DB_PORT=3306

### 6. Aplicar las migraciones
Ejecutar:
    py manage.py migrate

### 7. Crear un superusuario
Ejecutar:
    py manage.py createsuperuser
Completar los datos solicitados.

### 8. Ejecutar el servidor
Ejecutar:
    py manage.py runserver
El servidor estará disponible en:
    http://localhost:8000/
El panel de administración se encuentra en:
    http://localhost:8000/admin/

## Autenticación y permisos
La API utiliza autenticación mediante tokens.
Para obtener un token, enviar una solicitud POST a:

    http://localhost:8000/api/token/
Con el usuario y contraseña correspondientes.
Para acceder a los endpoints protegidos, enviar el encabezado:
    Authorization: Token <token_obtenido>
EcoGestión cuenta con tres grupos de usuarios: Administrador, Operador y Consulta.

| Operación | Administrador | Operador | Consulta |
|---|---|---|---|
| Consultar registros (GET) | Sí | Sí | Sí |
| Crear registros (POST) | Sí | Sí | No |
| Actualizar registros (PUT/PATCH) | Sí | Sí | No |
| Eliminar registros (DELETE) | Sí | No | No |
| Confirmar recolecciones | Sí | Sí | No |
| Cancelar recolecciones | Sí | Sí | No |
| Confirmar ventas | Sí | Sí | No |
| Anular ventas | Sí | Sí | No |
| Registrar pagos | Sí | Sí | No |

Los permisos se administran mediante los grupos y permisos de Django.

Todos los usuarios necesitan autenticarse mediante un token para acceder a los endpoints.

Si un usuario no está autenticado, se devuelve HTTP 401.
Si está autenticado, pero no tiene permisos, se devuelve HTTP 403.

Los permisos no permiten omitir las validaciones y reglas de negocio del sistema.


## Reglas de negocio

### 1. Personas

Regla 1: La identificación de cada persona debe ser única.

Regla 2: Una persona debe estar activa y tener el tipo PROVEEDOR o AMBOS para registrar recolecciones.

Regla 3: Una persona debe estar activa y tener el tipo COMPRADOR o AMBOS para registrar ventas.

### 2. Inventario

Regla 4: El nombre de cada material debe ser único.

Regla 5: El precio de venta por kilogramo debe ser mayor a cero.

Regla 6: El stock no puede modificarse directamente desde la API. Se actualiza mediante las confirmaciones de recolecciones y ventas.

### 3. Recolecciones

Regla 7: Las cantidades de los materiales recolectados deben ser mayores a cero.

Regla 8: Solamente se pueden agregar materiales activos a una recolección.

Regla 9: Solo se pueden modificar o eliminar recolecciones y detalles que estén pendientes.

Regla 10: Una recolección debe tener al menos un detalle para poder confirmarse.

Regla 11: Al confirmar una recolección, las cantidades recibidas se suman al inventario y su estado cambia a RECIBIDA.

Regla 12: Solamente se pueden cancelar recolecciones pendientes.

### 4. Ventas

Regla 13: Las cantidades y los precios unitarios de los detalles deben ser mayores a cero.

Regla 14: Solo se pueden modificar o eliminar ventas y detalles que estén pendientes.

Regla 15: Una venta debe contener al menos un detalle para poder confirmarse.

Regla 16: No se puede confirmar una venta si los materiales están inactivos o no existe suficiente stock.

Regla 17: Al confirmar una venta, las cantidades vendidas se descuentan del inventario y su estado cambia a CONFIRMADA.

Regla 18: El subtotal de cada detalle se calcula multiplicando la cantidad por el precio unitario. El total de la venta corresponde a la suma de sus subtotales.

Regla 19: Solamente se pueden anular ventas pendientes.

### 5. Pagos

Regla 20: El monto de cada pago debe ser mayor a cero.

Regla 21: Solamente se pueden registrar pagos de ventas confirmadas.

Regla 22: La suma de los pagos realizados no puede superar el total de la venta.

Regla 23: No se permite cambiar la venta asociada a un pago existente.


## Endpoints de la API
URL base: http://localhost:8000

### Autenticación
- POST /api/token/: Obtener token de acceso.

### Personas
- GET y POST /api/personas/: Listar y registrar personas.
- GET, PUT, PATCH y DELETE /api/personas/<id>/: Consultar, actualizar o eliminar personas.

### Inventario
- GET y POST /api/materiales/: Listar y registrar materiales.
- GET, PUT, PATCH y DELETE /api/materiales/<id>/: Consultar, actualizar o eliminar materiales.
- Filtros: categoria, activo, buscar, orden y page.
- Paginación: 5 materiales por página.

### Recolecciones
- GET y POST /api/recolecciones/: Listar y registrar recolecciones.
- GET, PUT, PATCH y DELETE /api/recolecciones/<id>/: Consultar, actualizar o eliminar recolecciones.
- POST /api/recolecciones/<id>/confirmar/: Confirmar recolección y aumentar inventario.
- POST /api/recolecciones/<id>/cancelar/: Cancelar una recolección.
- GET y POST /api/recolecciones/detalles/: Listar y registrar detalles.
- GET, PUT, PATCH y DELETE /api/recolecciones/detalles/<id>/: Consultar, actualizar o eliminar detalles.
- Filtros: estado, proveedor y page.
- Paginación: 5 recolecciones por página.

### Ventas
- GET y POST /api/ventas/: Listar y registrar ventas.
- GET, PUT, PATCH y DELETE /api/ventas/<id>/: Consultar, actualizar o eliminar ventas.
- POST /api/ventas/<id>/confirmar/: Confirmar venta y descontar inventario.
- POST /api/ventas/<id>/anular/: Anular una venta.
- GET y POST /api/ventas/detalles/: Listar y registrar detalles.
- GET, PUT, PATCH y DELETE /api/ventas/detalles/<id>/: Consultar, actualizar o eliminar detalles.
- Filtros: estado y comprador.

### Pagos
- GET y POST /api/pagos/: Listar y registrar pagos.
- GET, PUT, PATCH y DELETE /api/pagos/<id>/: Consultar, actualizar o eliminar pagos.
- Filtros: venta, comprador y metodo_pago.

### Autenticación y permisos
- TokenAuthentication: Autenticación mediante token.
- Administrador: Consultar, crear, modificar y eliminar.
- Operador: Consultar, crear y modificar.
- Consulta: Únicamente consultar.
- Header: Authorization: Token <token>

### Respuestas HTTP
- 200: Operación correcta.
- 201: Registro creado.
- 204: Registro eliminado.
- 400: Datos inválidos.
- 401: No autenticado.
- 403: Sin permisos.
- 404: Registro no encontrado.
- 409: Conflicto con una regla de negocio.


## Pruebas automatizadas
El proyecto incluye pruebas automatizadas para validar operaciones CRUD, reglas de negocio, autenticación y permisos.

Para ejecutar todas las pruebas:
    py manage.py test
Durante el desarrollo se ejecutaron satisfactoriamente 16 pruebas automatizadas.

## Integrantes del proyecto
- Pedro
- Stacy