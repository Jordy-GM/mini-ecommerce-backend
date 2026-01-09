Backend — Prueba Técnica React + Python (Mini Ecommerce)
1. Descripción General

Este repositorio corresponde exclusivamente al backend de la prueba técnica Mini Ecommerce.
El backend está desarrollado en Python con Django y Django REST Framework, y expone una API REST que es consumida por un frontend en React.

Sus responsabilidades principales son:

Gestión de productos

Gestión del carrito de compras

Persistencia de datos

Exposición de endpoints REST

2. Tecnologías Utilizadas

Python 3.11

Django

Django REST Framework

PostgreSQL (Docker) / SQLite (local)

Docker & Docker Compose

Makefile para automatización

pgAdmin (opcional)

Arquitectura modular por aplicaciones

3. ## Estructura del Proyecto (Backend)

```text
BACKEND/
├── cart/                     # Lógica del carrito
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── views.py
│   └── urls.py
│
├── products/                 # Gestión de productos
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── views.py
│   ├── urls.py
│   └── management/
│       └── commands/
│           └── populate_products.py
│
├── config/                   # Configuración principal de Django
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── docs/                     # Documentación (Swagger / OpenAPI)
│   ├── decorators/
│   ├── examples/
│   └── schemas/
│
├── venv/                     # Entorno virtual (local)
├── docker-compose.yml
├── dockerfile
├── makefile
├── manage.py
├── requirements.txt
└── .env

```
4. Endpoints Principales
Productos

GET /products/
Retorna el listado de productos disponibles.

Carrito

POST /cart/
Guarda un carrito con productos y cantidades en la base de datos.

(Pueden existir endpoints adicionales según la implementación)

5. Configuración Local (Sin Docker)
Requisitos

Python 3.11

Git

Sistema Windows (Makefile adaptado)

Pasos
cd backend
make setup
make install
make migrate-local
make populate-local
make dev


La aplicación quedará disponible en:

http://localhost:8000

6. Configuración con Docker (Recomendado)
Requisitos

Docker

Docker Compose

Setup completo automático
cd backend
make docker-setup


Este comando realiza:

Build de imágenes

Levanta contenedores

Ejecuta migraciones

Pobla productos iniciales

Servicios disponibles

Backend API
http://localhost:8000

pgAdmin
http://localhost:5050

Usuario: admin@admin.com
Contraseña: admin



6.1 Acceso y Configuración de pgAdmin

El proyecto incluye pgAdmin para administrar la base de datos PostgreSQL de forma visual cuando se ejecuta con Docker.

 Acceder a pgAdmin

Abre pgAdmin en tu navegador:

http://localhost:5050


Inicia sesión con las credenciales por defecto:

Email: admin@admin.com

Password: admin

Nota: Estas credenciales están definidas en el archivo docker-compose.yml.

 Configurar la conexión a la base de datos

Una vez dentro de pgAdmin, debes registrar el servidor de PostgreSQL.

Pasos para registrar el servidor

En el panel izquierdo, haz clic derecho sobre Servers

Selecciona Register → Server…

Pestaña General

Name:
Django App Ecommerce (o el nombre que prefieras)

Pestaña Connection

Host name/address:
postgres_app_commerce
 Importante: debe ser el nombre del contenedor, NO localhost

Port: 5432

Maintenance database: postgres

Username: postgres

Password: 14251425

Save password:  Marcar esta opción

Finalmente, haz clic en Save.

 Persistencia de la configuración en pgAdmin

pgAdmin guarda automáticamente la información del servidor registrado, por lo que:

 La conexión queda guardada

 La contraseña se conserva (si marcaste Save password)

 Solo necesitarás iniciar sesión en pgAdmin en futuras ejecuciones

 Cuándo debes volver a configurar pgAdmin

Solo será necesario volver a registrar el servidor en los siguientes casos:

Si eliminas el contenedor de pgAdmin

Si cambias las credenciales de PostgreSQL

Si ejecutas docker-compose down -v (elimina los volúmenes)



7. Comandos Útiles del Makefile
Desarrollo Local
make setup
make install
make dev
make migrate-local
make populate-local

Docker
make docker-up
make docker-down
make docker-logs
make docker-ps
make docker-reset

Base de Datos (Docker)
make migrate
make makemigrations
make populate-db
make createsuperuser

Testing
make test
make test-docker

8. Persistencia del Carrito

El frontend mantiene el carrito en localStorage.

Al presionar Guardar carrito, los datos se envían al backend.

El backend persiste el carrito en la base de datos.

Se retorna un mensaje de confirmación al usuario.

9. Documentación de la API

La carpeta /docs está preparada para documentación Swagger / OpenAPI, incluyendo:

Esquemas (schemas)

Ejemplos (examples)

Decoradores (decorators)

Puede integrarse fácilmente con herramientas como:

drf-spectacular

drf-yasg

10. Buenas Prácticas Aplicadas

Separación por capas (views, services, serializers)

Arquitectura modular por apps

Uso de comandos personalizados de Django

Automatización mediante Makefile

Soporte completo para Docker

Código claro, mantenible y escalable

11. Alcance de la Prueba Técnica

Este backend cumple con los requisitos definidos en la prueba:

✔ Listado de productos desde API

✔ Gestión completa del carrito

✔ Persistencia en base de datos

✔ Comunicación frontend-backend

✔ Estructura clara y profesional

12. Nota Final

Este repositorio corresponde únicamente al backend.
El frontend debe ejecutarse por separado y consumir esta API.
