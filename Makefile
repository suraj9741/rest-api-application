# ===== CONFIG =====
VENV_PATH=~/py_env/student
PYTHON=python3
PIP=$(VENV_PATH)/bin/pip
PYTHON_BIN=$(VENV_PATH)/bin/python
FLASK_APP=manage:create_app
COMPOSE_FILE=postgres.yaml
SERVICE_NAME=postgres_db

# ===== CHECK DOCKER CONTAINER =====
check-db:
	@echo "🔍 Checking Postgres container..."
	@if [ "$$(docker ps -q -f name=db)" ]; then \
		echo "✅ Postgres is already running"; \
	else \
		echo "🚀 Starting Postgres container..."; \
		docker compose -f $(COMPOSE_FILE) up -d; \
	fi

# ===== SETUP VENV =====
venv:
	@echo "🐍 Setting up virtual environment..."

	# Expand ~ properly
	@VENV_DIR=$(VENV_PATH); \
	VENV_DIR=$${VENV_DIR/#\~/$$HOME}; \
	\
	if [ ! -d "$$VENV_DIR" ]; then \
		echo "📁 Creating directory $$VENV_DIR"; \
		mkdir -p $$VENV_DIR; \
	fi; \
	\
	if [ ! -d "$$VENV_DIR/bin" ]; then \
		echo "⚙️ Creating virtual environment..."; \
		$(PYTHON) -m venv $$VENV_DIR; \
	else \
		echo "Virtual environment already exists"; \
	fi

# ===== ACTIVATE VENV =====
activate:
	@VENV_DIR=$(VENV_PATH); \
	VENV_DIR=$${VENV_DIR/#\~/$$HOME}; \
	source $$VENV_DIR/bin/activate && echo "Activated"

# ===== INSTALL DEPENDENCIES =====
install: venv
	@echo "📦 Installing dependencies..."
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt

# ===== RUN TESTS =====
test: install check-db
	@echo "🧪 Running tests..."
	@PYTHONPATH=. $(PYTHON_BIN) -m pytest -v

# ===== RUN APP =====
run: install check-db
	@echo "🚀 Starting application..."
	@$(PYTHON_BIN) run.py

# ===== STOP DB =====
stop-db:
	@echo "🛑 Stopping Postgres..."
	@docker compose -f $(COMPOSE_FILE) down

# ===== CLEAN =====
clean:
	@echo "🧹 Cleaning cache..."
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@find . -type f -name "*.pyc" -delete

# ===== STOP APP =====
stop-app:
	@echo "🛑 Stopping application..."
	@pkill -f "run.py" || echo "⚠️ App not running"

# ===== STOP ALL =====
stop-all:
	@echo "🛑 Stopping application..."
	@pkill -f "run.py" || echo "⚠️ App not running"

	@echo "🛑 Stopping Postgres..."
	@docker compose -f $(COMPOSE_FILE) down

	@echo "🧹 Cleaning temp files..."
	@find . -type d -name "__pycache__" -exec rm -r {} + || true
	@find . -type f -name "*.pyc" -delete || true

	@echo "✅ All resources stopped"

# ==== DB MIGRATION =====
migrate:
	@echo "📦 Generating migration..."
	@$(PYTHON_BIN) -m flask db migrate -m "auto migration"

# ==== DB UPGRADE =====
upgrade:
	@echo "🚀 Applying migration..."
	@$(PYTHON_BIN) -m flask db upgrade

# ===== ALL-IN-ONE =====
all: venv activate install check-db upgrade test run
	@echo "🎉 All tasks completed!"