.PHONY: setup install dev run test clean help docker-up docker-down docker-logs populate-db

# Configuración
PYTHON := python
VENV := venv
VENV_BIN := $(VENV)\Scripts
PORT := 8000
DOCKER_COMPOSE := docker-compose
BACKEND_SERVICE := web

help:
	@echo Comandos disponibles:
	@echo   make setup              - Crear entorno virtual
	@echo   make install            - Instalar dependencias
	@echo   make dev                - Iniciar servidor Django en desarrollo
	@echo   make test               - Ejecutar tests
	@echo   make clean              - Limpiar archivos temporales
	@echo   make docker-up          - Levantar contenedores Docker
	@echo   make docker-down        - Detener contenedores Docker
	@echo   make docker-logs        - Ver logs de contenedores
	@echo   make populate-db        - Poblar base de datos en Docker
	@echo   make migrate            - Ejecutar migraciones en Docker
	@echo   make makemigrations     - Crear migraciones en Docker
	@echo   make docker-setup       - Setup completo Docker
	@echo   make docker-reset       - Reiniciar todo (down + up + migrate + populate)

# Crear entorno virtual
setup:
	@echo Creando entorno virtual...
	$(PYTHON) -m venv $(VENV)
	@echo Entorno virtual creado en .\$(VENV)
	@echo Activalo con: .\$(VENV_BIN)\Activate.ps1

# Instalar dependencias
install:
	@echo Instalando dependencias...
	$(VENV_BIN)\python.exe -m pip install --upgrade pip
	@if exist requirements.txt ( \
		$(VENV_BIN)\pip.exe install -r requirements.txt && \
		echo Dependencias instaladas desde requirements.txt \
	) else ( \
		echo No se encontro requirements.txt \
	)

# Desarrollo local: inicia servidor Django con hot-reload
dev:
	@if not exist "$(VENV)" ( \
		echo No existe entorno virtual. Creandolo... && \
		$(MAKE) setup && \
		$(MAKE) install \
	)
	@echo Iniciando servidor Django en modo desarrollo...
	$(VENV_BIN)\python.exe manage.py runserver 0.0.0.0:$(PORT)

# Migraciones locales
migrate-local:
	@echo Ejecutando migraciones localmente...
	$(VENV_BIN)\python.exe manage.py migrate

# Crear migraciones locales
makemigrations-local:
	@echo Creando migraciones localmente...
	$(VENV_BIN)\python.exe manage.py makemigrations

# Poblar DB localmente
populate-local:
	@echo Poblando base de datos localmente...
	$(VENV_BIN)\python.exe manage.py populate_products

# === COMANDOS DOCKER ===

# Levantar contenedores
docker-up:
	@echo Levantando contenedores Docker...
	$(DOCKER_COMPOSE) up -d
	@echo Contenedores iniciados

# Detener contenedores
docker-down:
	@echo Deteniendo contenedores Docker...
	$(DOCKER_COMPOSE) down
	@echo Contenedores detenidos

# Ver logs
docker-logs:
	$(DOCKER_COMPOSE) logs -f

# Ver logs del backend
docker-logs-web:
	$(DOCKER_COMPOSE) logs -f $(BACKEND_SERVICE)

# Ver logs de la base de datos
docker-logs-db:
	$(DOCKER_COMPOSE) logs -f db

# Rebuild de contenedores
docker-rebuild:
	@echo Reconstruyendo contenedores...
	$(DOCKER_COMPOSE) up -d --build
	@echo Contenedores reconstruidos

# Ver estado de contenedores
docker-ps:
	@echo Estado de los contenedores:
	@$(DOCKER_COMPOSE) ps

# === COMANDOS DE BASE DE DATOS EN DOCKER ===

# Crear migraciones en Docker
makemigrations:
	@echo Creando migraciones en Docker...
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py makemigrations
	@echo Migraciones creadas

# Ejecutar migraciones en Docker
migrate:
	@echo Ejecutando migraciones en Docker...
	@echo Esperando a que la base de datos este lista...
	@timeout /t 3 /nobreak >nul
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py migrate
	@echo Migraciones aplicadas

# Poblar base de datos en Docker
populate-db:
	@echo Poblando base de datos con productos en Docker...
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py populate_products
	@echo Base de datos poblada exitosamente

# Crear superusuario
createsuperuser:
	@echo Creando superusuario...
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py createsuperuser

# Setup completo de Docker (levantar + migrar + poblar)
docker-setup: docker-up
	@echo Esperando que los contenedores esten completamente listos...
	@timeout /t 15 /nobreak >nul
	@echo.
	@echo Verificando estado de contenedores...
	@$(MAKE) docker-ps
	@echo.
	@$(MAKE) migrate
	@echo.
	@$(MAKE) populate-db
	@echo.
	@echo ========================================
	@echo Setup de Docker completado exitosamente
	@echo ========================================
	@echo Aplicacion disponible en: http://localhost:8000
	@echo pgAdmin disponible en: http://localhost:5050

# Reiniciar todo desde cero
docker-reset: docker-down
	@echo Eliminando volumenes...
	$(DOCKER_COMPOSE) down -v
	@echo Levantando contenedores...
	$(DOCKER_COMPOSE) up -d --build
	@echo Esperando que los contenedores esten listos...
	@timeout /t 15 /nobreak >nul
	@$(MAKE) migrate
	@$(MAKE) populate-db
	@echo Reset completado

# Shell de Django en Docker
shell:
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py shell

# Shell interactivo de Python en Docker
shell-plus:
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py shell_plus

# Acceder al bash del contenedor
bash:
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) /bin/bash

# Conectarse a PostgreSQL
db-shell:
	$(DOCKER_COMPOSE) exec db psql -U postgres -d app_commerce

# Ejecutar tests locales
test:
	@echo Ejecutando tests...
	$(VENV_BIN)\python.exe manage.py test

# Ejecutar tests en Docker
test-docker:
	@echo Ejecutando tests en Docker...
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py test

# Ver archivos estáticos
collectstatic:
	@echo Recolectando archivos estaticos...
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py collectstatic --noinput

# Limpiar archivos temporales
clean:
	@echo Limpiando archivos temporales...
	@for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
	@for /r . %%f in (*.pyc) do @if exist "%%f" del /q "%%f"
	@for /d /r . %%d in (*.egg-info) do @if exist "%%d" rd /s /q "%%d"
	@for /d /r . %%d in (.pytest_cache) do @if exist "%%d" rd /s /q "%%d"
	@echo Limpieza completada

# Eliminar entorno virtual
clean-all: clean
	@echo Eliminando entorno virtual...
	@if exist "$(VENV)" rd /s /q "$(VENV)"
	@echo Entorno virtual eliminado

# Limpiar Docker (contenedores + volúmenes)
docker-clean:
	@echo Limpiando contenedores y volumenes Docker...
	$(DOCKER_COMPOSE) down -v
	@echo Limpieza de Docker completada

# Reiniciar contenedor web
docker-restart-web:
	@echo Reiniciando contenedor web...
	$(DOCKER_COMPOSE) restart $(BACKEND_SERVICE)
	@echo Contenedor reiniciado

# Reiniciar contenedor db
docker-restart-db:
	@echo Reiniciando contenedor de base de datos...
	$(DOCKER_COMPOSE) restart db
	@echo Contenedor de base de datos reiniciado