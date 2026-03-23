# ===== CONFIG =====
VENV_PATH=/Users/one2n/py_env/student
PYTHON=python3
PIP=$(VENV_PATH)/bin/pip
PYTHON_BIN=$(VENV_PATH)/bin/python

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
	@if [ ! -d "$(VENV_PATH)" ]; then \
		$(PYTHON) -m venv $(VENV_PATH); \
	fi

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

# ===== ALL-IN-ONE =====
all: test run

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