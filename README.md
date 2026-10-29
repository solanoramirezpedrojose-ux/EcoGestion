EcoGestión
Sistema de gestión para un centro de acopio y reciclaje, desarrollado con Python, Django, Django REST Framework y MySQL.
1. Descripción del proyecto
EcoGestión es una API REST que permite administrar las operaciones de un centro de acopio y reciclaje, incluyendo el registro de personas, el control de materiales reciclables, las recolecciones, las ventas y los pagos.

El sistema permite controlar el inventario de materiales, registrar operaciones y gestionar el acceso a los recursos mediante autenticación por tokens y permisos de usuario.
2. Tecnologías utilizadas
- Python 3.13
- Django 5.2
- Django REST Framework
- MySQL
- MySQL Workbench
- TokenAuthentication
- Postman
- Git y GitHub
- Visual Studio Code
3. Módulos del sistema
Personas: Administración de proveedores y compradores.

Inventario: Registro de materiales reciclables, precios y cantidades disponibles.

Recolecciones: Registro de materiales recibidos y actualización del inventario.

Ventas: Registro de ventas, detalles y descuento de materiales del inventario.

Pagos: Registro y administración de pagos asociados a las ventas.
4. Diagrama entidad-relación
El siguiente diagrama representa los siete modelos del sistema EcoGestión, sus atributos, claves primarias, claves foráneas y relaciones.

Las relaciones principales son:
- Persona - Recolección: Una persona puede registrar varias recolecciones.
- Persona - Venta: Una persona puede realizar varias compras.
- Recolección - DetalleRecolección: Una recolección puede contener varios detalles.
- Material - DetalleRecolección: Un material puede aparecer en diferentes recolecciones.
- Venta - DetalleVenta: Una venta puede contener varios detalles.
- Material - DetalleVenta: Un material puede aparecer en diferentes ventas.
- Venta - Pago: Una venta puede tener varios pagos.
5. Requisitos previos
Para ejecutar EcoGestión es necesario contar con:
- Python instalado.
- MySQL Server instalado y funcionando.
- MySQL Workbench para administrar la base de datos.
- Visual Studio Code o cualquier editor de código.
- Acceso a una terminal.
- Credenciales de un usuario MySQL con permisos sobre la base de datos.
Postman se utiliza para realizar las pruebas de la API.
6. Instalación y configuración
6.1. Obtener el proyecto
Clonar el repositorio desde GitHub o descargar el proyecto en formato ZIP.

Abrir la carpeta principal de EcoGestión en Visual Studio Code, donde se encuentra el archivo manage.py.
6.2. Crear el entorno virtual
Desde la terminal de VS Code, ejecutar:
py -m venv .venv
Activar el entorno virtual en PowerShell:
.\.venv\Scripts\Activate.ps1
Cuando el entorno esté activado, debe aparecer (.venv) al inicio de la terminal.
6.3. Instalar las dependencias
Actualizar pip:
python -m pip install --upgrade pip
La forma recomendada de instalar todas las dependencias del proyecto es:
pip install -r requirements.txt
Este comando instala automáticamente las bibliotecas necesarias con las versiones indicadas en requirements.txt.

También es posible instalarlas manualmente mediante los siguientes comandos:

Instalar Django:
pip install Django==5.2.18
Instalar Django REST Framework:
pip install djangorestframework==3.18.3
Instalar MySQL Client:
pip install mysqlclient==2.3.0
Instalar python-dotenv:
pip install python-dotenv==1.2.4
No es necesario ejecutar los comandos individuales si ya se utilizó correctamente pip install -r requirements.txt.

Para verificar las instalaciones:
py -m django --version
pip list
6.4. Configurar la base de datos MySQL
Abrir MySQL Workbench y conectarse con un usuario que tenga permisos para crear bases de datos y usuarios.

Crear la base de datos:
CREATE DATABASE IF NOT EXISTS ecogestion_db;
Crear un usuario para el proyecto, si todavía no existe:
CREATE USER 'ecogestion_user'@'localhost'

IDENTIFIED BY 'tu_contrasena_segura';
Asignar permisos sobre la base de datos:
GRANT ALL PRIVILEGES ON ecogestion_db.*

TO 'ecogestion_user'@'localhost';
Para ejecutar las pruebas automatizadas de Django con MySQL, el usuario también necesita permisos sobre la base de datos temporal de pruebas:
GRANT ALL PRIVILEGES ON test_ecogestion_db.*

TO 'ecogestion_user'@'localhost';
Estos comandos son ejemplos de configuración inicial. Si la base de datos y el usuario ya existen, no es necesario crearlos nuevamente.
6.5. Configurar las variables de entorno
El proyecto utiliza un archivo .env para almacenar las credenciales de MySQL.

Copiar el archivo .env.example y guardar la copia con el nombre .env.

Configurar los datos correspondientes:
DB_NAME=ecogestion_db

DB_USER=usuario_mysql

DB_PASSWORD=contrasena_mysql

DB_HOST=localhost

DB_PORT=3306
Se deben reemplazar los valores de ejemplo por las credenciales de MySQL configuradas en la computadora.

El archivo .env contiene información privada y no debe subirse a GitHub.
6.6. Generar y aplicar las migraciones
Para detectar cambios en los modelos:
py manage.py makemigrations
Para aplicar las migraciones a MySQL:
py manage.py migrate
Las migraciones incluidas en el repositorio permiten crear las tablas del sistema.
6.7. Crear un superusuario
Ejecutar:
py manage.py createsuperuser
Completar el nombre de usuario, correo electrónico si se solicita y contraseña.

El superusuario permite ingresar al administrador de Django y configurar los grupos y permisos.
6.8. Configurar grupos y usuarios
Ingresar al panel de administración:

http://localhost:8000/admin/

Crear los siguientes grupos en la sección Grupos:

Administrador: Permisos para consultar, crear, modificar y eliminar registros.

Operador: Permisos para consultar, crear y modificar registros.

Consulta: Permisos únicamente para consultar registros.

Asignar a cada grupo los permisos correspondientes de los modelos:
- Persona
- Material
- Recoleccion
- DetalleRecoleccion
- Venta
- DetalleVenta
- Pago
Posteriormente, crear o asignar usuarios a los grupos correspondientes.
6.9. Ejecutar el servidor
Ejecutar:
py manage.py runserver
Servidor de desarrollo:

http://localhost:8000/

Panel de administración:

http://localhost:8000/admin/

Para detener el servidor, presionar Ctrl + C en la terminal.
7. Autenticación y permisos
La API utiliza TokenAuthentication de Django REST Framework.

Para obtener un token, enviar una solicitud POST a:

http://localhost:8000/api/token/

Body JSON:
{

  "username": "tu_usuario",

  "password": "tu_contrasena"

}
Una vez obtenido el token, agregar el siguiente encabezado en las solicitudes protegidas:
Authorization: Token TU_TOKEN
Matriz de permisos
Operación	Administrador	Operador	Consulta
Consultar registros (GET)	Sí	Sí	Sí
Crear registros (POST)	Sí	Sí	No
Actualizar registros (PUT/PATCH)	Sí	Sí	No
Eliminar registros (DELETE)	Sí	No	No
Confirmar recolecciones	Sí	Sí	No
Cancelar recolecciones	Sí	Sí	No
Confirmar ventas	Sí	Sí	No
Anular ventas	Sí	Sí	No
Registrar pagos	Sí	Sí	No


Los permisos se administran mediante los grupos y permisos nativos de Django.

Los endpoints del sistema requieren autenticación mediante token.

Un usuario sin autenticación recibe HTTP 401.

Un usuario autenticado, pero sin los permisos necesarios, recibe HTTP 403.

Las reglas de negocio deben cumplirse independientemente de los permisos del usuario.
8. Reglas de negocio
8.1. Personas
Regla 1: La identificación de cada persona debe ser única.

Regla 2: Una persona debe estar activa y tener el tipo PROVEEDOR o AMBOS para registrar recolecciones.

Regla 3: Una persona debe estar activa y tener el tipo COMPRADOR o AMBOS para registrar ventas.
8.2. Inventario
Regla 4: El nombre de cada material debe ser único.

Regla 5: El precio de venta por kilogramo debe ser mayor a cero.

Regla 6: El stock no puede modificarse directamente desde la API. Se actualiza mediante las confirmaciones de recolecciones y ventas.
8.3. Recolecciones
Regla 7: Las cantidades de los materiales recolectados deben ser mayores a cero.

Regla 8: Solamente se pueden agregar materiales activos a una recolección.

Regla 9: Solo se pueden modificar o eliminar recolecciones y detalles que estén pendientes.

Regla 10: Una recolección debe tener al menos un detalle para poder confirmarse.

Regla 11: Al confirmar una recolección, las cantidades recibidas se suman al inventario y su estado cambia a RECIBIDA.

Regla 12: Solamente se pueden cancelar recolecciones pendientes.
8.4. Ventas
Regla 13: Las cantidades y los precios unitarios de los detalles deben ser mayores a cero.

Regla 14: Solo se pueden modificar o eliminar ventas y detalles que estén pendientes.

Regla 15: Una venta debe contener al menos un detalle para poder confirmarse.

Regla 16: No se puede confirmar una venta si los materiales están inactivos o no existe suficiente stock.

Regla 17: Al confirmar una venta, las cantidades vendidas se descuentan del inventario y su estado cambia a CONFIRMADA.

Regla 18: El subtotal de cada detalle se calcula multiplicando la cantidad por el precio unitario. El total de la venta corresponde a la suma de sus subtotales.

Regla 19: Solamente se pueden anular ventas pendientes.
8.5. Pagos
Regla 20: El monto de cada pago debe ser mayor a cero.

Regla 21: Solamente se pueden registrar pagos de ventas confirmadas.

Regla 22: La suma de los pagos realizados no puede superar el total de la venta.

Regla 23: No se permite cambiar la venta asociada a un pago existente.
9. Endpoints de la API
URL base: http://localhost:8000
9.1. Autenticación
- POST /api/token/: Obtener token de acceso.
9.2. Personas
- GET /api/personas/: Listar personas.
- POST /api/personas/: Registrar persona.
- GET /api/personas/<id>/: Consultar persona.
- PUT /api/personas/<id>/: Actualizar persona.
- PATCH /api/personas/<id>/: Actualizar parcialmente.
- DELETE /api/personas/<id>/: Eliminar persona.
9.3. Inventario
- GET /api/materiales/: Listar materiales.
- POST /api/materiales/: Registrar material.
- GET /api/materiales/<id>/: Consultar material.
- PUT /api/materiales/<id>/: Actualizar material.
- PATCH /api/materiales/<id>/: Actualizar parcialmente.
- DELETE /api/materiales/<id>/: Eliminar material.
Filtros disponibles:
- ?categoria=METAL: Filtrar por categoría.
- ?activo=true: Filtrar materiales activos.
- ?buscar=aluminio: Buscar materiales por nombre.
- ?orden=nombre: Ordenar por nombre.
- ?orden=-precio_venta_kg: Ordenar por precio descendente.
- ?page=1: Consultar una página.
Paginación: 5 materiales por página.
9.4. Recolecciones
- GET /api/recolecciones/: Listar recolecciones.
- POST /api/recolecciones/: Registrar recolección.
- GET /api/recolecciones/<id>/: Consultar recolección.
- PUT /api/recolecciones/<id>/: Actualizar recolección.
- PATCH /api/recolecciones/<id>/: Actualizar parcialmente.
- DELETE /api/recolecciones/<id>/: Eliminar recolección.
- POST /api/recolecciones/<id>/confirmar/: Confirmar recolección y aumentar inventario.
- POST /api/recolecciones/<id>/cancelar/: Cancelar recolección.
Detalles de recolección:
- GET /api/recolecciones/detalles/: Listar detalles.
- POST /api/recolecciones/detalles/: Registrar detalle.
- GET /api/recolecciones/detalles/<id>/: Consultar detalle.
- PUT /api/recolecciones/detalles/<id>/: Actualizar detalle.
- PATCH /api/recolecciones/detalles/<id>/: Actualizar parcialmente.
- DELETE /api/recolecciones/detalles/<id>/: Eliminar detalle.
Filtros disponibles:
- ?estado=PENDIENTE: Filtrar por estado.
- ?proveedor=1: Filtrar por proveedor.
- ?page=1: Consultar una página.
- /api/recolecciones/detalles/?recoleccion=1: Consultar detalles de una recolección.
Paginación: 5 recolecciones por página.
9.5. Ventas
- GET /api/ventas/: Listar ventas.
- POST /api/ventas/: Registrar venta.
- GET /api/ventas/<id>/: Consultar venta.
- PUT /api/ventas/<id>/: Actualizar venta.
- PATCH /api/ventas/<id>/: Actualizar parcialmente.
- DELETE /api/ventas/<id>/: Eliminar venta.
- POST /api/ventas/<id>/confirmar/: Confirmar venta y descontar inventario.
- POST /api/ventas/<id>/anular/: Anular venta.
Detalles de venta:
- GET /api/ventas/detalles/: Listar detalles.
- POST /api/ventas/detalles/: Registrar detalle.
- GET /api/ventas/detalles/<id>/: Consultar detalle.
- PUT /api/ventas/detalles/<id>/: Actualizar detalle.
- PATCH /api/ventas/detalles/<id>/: Actualizar parcialmente.
- DELETE /api/ventas/detalles/<id>/: Eliminar detalle.
Filtros disponibles:
- ?estado=PENDIENTE: Filtrar ventas por estado.
- ?comprador=1: Filtrar ventas por comprador.
- /api/ventas/detalles/?venta=1: Consultar detalles de una venta.
9.6. Pagos
- GET /api/pagos/: Listar pagos.
- POST /api/pagos/: Registrar pago.
- GET /api/pagos/<id>/: Consultar pago.
- PUT /api/pagos/<id>/: Actualizar pago.
- PATCH /api/pagos/<id>/: Actualizar parcialmente.
- DELETE /api/pagos/<id>/: Eliminar pago.
Filtros disponibles:
- ?venta=1: Filtrar por venta.
- ?comprador=1: Filtrar por comprador.
- ?metodo_pago=EFECTIVO: Filtrar por método de pago.
10. Códigos de respuesta HTTP
- 200 OK: Operación realizada correctamente.
- 201 Created: Registro creado correctamente.
- 204 No Content: Registro eliminado correctamente.
- 400 Bad Request: Datos inválidos o error de validación.
- 401 Unauthorized: Usuario no autenticado.
- 403 Forbidden: Usuario sin permisos suficientes.
- 404 Not Found: Registro inexistente.
- 409 Conflict: Operación que incumple una regla de negocio.
11. Pruebas automatizadas
El proyecto incluye pruebas automatizadas para validar las operaciones CRUD, reglas de negocio, autenticación y permisos.

Durante el desarrollo se ejecutaron satisfactoriamente 16 pruebas automatizadas.

Para ejecutar todas las pruebas:
py manage.py test
Para ejecutar las pruebas de un módulo específico:
py manage.py test personas
py manage.py test inventario
py manage.py test recolecciones
py manage.py test ventas
Las pruebas de Django utilizan una base de datos temporal y no deben modificar los registros de producción.
12. Pruebas con Postman
El proyecto cuenta con una colección de Postman utilizada para probar los endpoints de EcoGestión.

Se realizaron 60 solicitudes de prueba para verificar operaciones CRUD, autenticación, permisos, filtros, reglas de negocio y respuestas HTTP. La colección exportada contiene 61 solicitudes, incluyendo una adicional para obtener el token del grupo Consulta.

El archivo de la colección debe incluirse en el proyecto en la siguiente ubicación:

postman/EcoGestion_API.postman_collection.json
Solicitudes documentadas de Postman
La colección EcoGestion API contiene 61 solicitudes. A continuación se documentan 20 representativas con sus respuestas esperadas.
1. Obtener Token: POST /api/token/ — 200 OK. Autenticar un usuario y obtener su token.
2. Listar Personas: GET /api/personas/ — 200 OK. Consultar las personas registradas.
3. Registrar Persona: POST /api/personas/ — 201 Created. Registrar un proveedor o comprador.
4. Persona Duplicada: POST /api/personas/ — 400 Bad Request. Rechazar una identificación que ya existe.
5. Persona Inexistente: GET /api/personas/9999/ — 404 Not Found. Comprobar el manejo de registros inexistentes.
6. Acceso Sin Token: GET /api/personas/ — 401 Unauthorized. Rechazar solicitudes sin autenticación.
7. Listar Materiales: GET /api/materiales/ — 200 OK. Consultar materiales con paginación.
8. Registrar Material: POST /api/materiales/ — 201 Created. Registrar un material reciclable.
9. Actualizar Material: PUT /api/materiales/2/ — 200 OK. Modificar los datos y el precio de un material.
10. Registrar Recolección: POST /api/recolecciones/ — 201 Created. Crear una recolección en estado PENDIENTE.
11. Registrar Detalle Recolección: POST /api/recolecciones/detalles/ — 201 Created. Registrar los kilogramos de material recolectado.
12. Confirmar Recolección: POST /api/recolecciones/1/confirmar/ — 200 OK. Confirmar la recepción y aumentar el inventario.
13. Verificar Stock: GET /api/materiales/1/ — 200 OK. Comprobar el aumento del stock de aluminio a 30 kg.
14. Recolección Ya Confirmada: POST /api/recolecciones/1/confirmar/ — 409 Conflict. Impedir que una recolección se confirme dos veces.
15. Eliminar Recolección Pendiente: DELETE /api/recolecciones/2/ — 204 No Content. Eliminar una recolección que todavía está pendiente.
16. Registrar Venta: POST /api/ventas/ — 201 Created. Registrar una venta para un comprador activo.
17. Registrar Detalle Venta: POST /api/ventas/detalles/ — 201 Created. Registrar material, cantidad y precio de venta.
18. Confirmar Venta: POST /api/ventas/1/confirmar/ — 200 OK. Confirmar una venta y descontar materiales del inventario.
19. Registrar Pago: POST /api/pagos/ — 201 Created. Registrar un pago asociado a una venta confirmada.
20. Crear Material Sin Permiso: POST /api/materiales/ — 403 Forbidden. Comprobar que el grupo Consulta no puede crear materiales.
Los datos enviados en el Body de cada solicitud se encuentran guardados en la colección de Postman.

Los identificadores utilizados corresponden a los registros de prueba y pueden cambiar en otra instalación.
Importar la colección
1. Abrir Postman.
2. Seleccionar Import.
3. Buscar el archivo JSON dentro de la carpeta postman.
4. Importar la colección.
5. Ejecutar el servidor Django.
6. Obtener un token de autenticación mediante /api/token/.
7. Configurar los encabezados de autenticación.
8. Ejecutar las solicitudes correspondientes.
Para probar las operaciones administrativas se utiliza un superusuario de Django.

Para comprobar los errores 403 se utiliza un usuario del grupo Consulta, sin permisos de escritura.
13. Consideraciones técnicas
El sistema utiliza permisos nativos de Django, autenticación por tokens y validaciones en los serializers y vistas.

Los archivos .env, .venv y otros archivos privados del entorno local no deben incluirse en el repositorio.
14. Integrantes del proyecto
- Pedro
- Stacy