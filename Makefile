# ===== CONFIG =====
# Load variables from .env
include .env
export $(shell sed 's/=.*//' .env)

# Default values (fallback if not in .env)
VENV_PATH ?=~/py_env/student
PYTHON=python3
PIP=$(VENV_PATH)/bin/pip
PYTHON_BIN=$(VENV_PATH)/bin/python
APPLICATION_IMAGE ?= my-app
DOCKER_USERNAME ?= user
APPLICATION_IMAGE_TAG ?= latest
IMAGE := $(DOCKER_USERNAME)/$(APPLICATION_IMAGE):$(APPLICATION_IMAGE_TAG)

# ===== CHECK/START DB DOCKER CONTAINER =====
start-db:
	@echo "🔍 Checking Postgres container..."
	@if [ "$$(docker ps -q -f name=db)" ]; then \
		echo "Postgres is already running"; \
	else \
		echo "Starting Postgres container..."; \
		docker compose up -d postgres_db; \
	fi
	@echo "⏳ Waiting for DB to be ready..."
	@until pg_isready -h localhost -p 5432 >/dev/null 2>&1; do \
		sleep 2; \
	done
	@echo "DB is ready!"

# ===== SETUP VENV =====
venv:
	@echo "🐍 Setting up virtual environment..."

	# Expand ~ properly
	@VENV_DIR=$(VENV_PATH); \
	VENV_DIR=$${VENV_DIR/#\~/$$HOME}; \
	\
	if [ ! -d "$$VENV_DIR" ]; then \
		echo "Creating directory $$VENV_DIR"; \
		mkdir -p $$VENV_DIR; \
	fi; \
	\
	if [ ! -d "$$VENV_DIR/bin" ]; then \
		echo "Creating virtual environment..."; \
		$(PYTHON) -m venv $$VENV_DIR; \
	else \
		echo "Virtual environment already exists"; \
	fi

# ===== ACTIVATE VENV =====
activate: venv
	@VENV_DIR=$(VENV_PATH); \
	VENV_DIR=$${VENV_DIR/#\~/$$HOME}; \
	source $$VENV_DIR/bin/activate && echo "Activated"

# ==== DB MIGRATION =====
migrate: start-db activate install upgrade
	@echo "Generating migration..."
	@$(PYTHON_BIN) -m flask db migrate -m "auto migration"

# ==== DB UPGRADE =====
upgrade: start-db activate install
	@echo "Applying migration..."
	@$(PYTHON_BIN) -m flask db upgrade

# ==== BUILD ====
build:
	@echo "Building Docker image..."
	@docker build -t $(IMAGE) .
	@echo "Build complete: $(IMAGE)"

# ==== PUSH ====
push: build
	@echo "Pushing image to Docker Hub..."
	@docker login
	@docker push $(IMAGE)
	@echo "Image pushed: $(IMAGE)"

# ===== INSTALL DEPENDENCIES =====
install: venv
	@echo "📦 Installing dependencies..."
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt

# ===== RUN TESTS =====
test:
	@echo "Running tests..."
	@docker compose --profile test up test

# ===== RUN APP =====
start-app:
	@echo "Starting application..."
	@docker compose up -d

# ===== STOP DB =====
stop-db:
	@echo "Stopping Postgres..."
	@docker compose down postgres_db

# ===== STOP APP =====
stop-app:
	@echo "Stopping application..."
	@docker compose down app || echo "App not running"

# ===== RUN APP =====
run: install start-db
	@echo "Starting application..."
	@$(PYTHON_BIN) app.py

# ===== python run =====
p-all: venv activate install start-db upgrade test run
	@echo "All tasks completed!"

# ===== STOP ALL =====
p-stop-all:
	@echo "Stopping application..."
	@pkill -f "app.py" || echo "App not running"

	@echo "Stopping Postgres..."
	@docker compose  -p student down

	@echo "Cleaning temp files..."
	@find . -type d -name "__pycache__" -exec rm -r {} + || true
	@find . -type f -name "*.pyc" -delete || true

	@echo "All resources stopped"

# ===== docker run =====
all: push
	@docker compose up -d
	@echo "All tasks completed!"

# ===== DOCKER STOP ALL =====
stop-all:
	@echo "Stopping all resources..."
	@docker compose  -p student down