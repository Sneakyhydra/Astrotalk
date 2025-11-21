.PHONY: install install-dev setup isort format lint check clean test help

VENV := ./venv
BIN := $(VENV)/bin

PYTHON_DIRS := database embedding languages model __init__.py main.py

# ------------------------------------------------------------------------------
# Environment Setup
# ------------------------------------------------------------------------------
setup:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	@echo "Virtual environment created at $(VENV)"

# ------------------------------------------------------------------------------
# Installation
# ------------------------------------------------------------------------------
install: setup
	@echo "Installing production dependencies..."
	$(BIN)/pip install -r requirements.txt

install-dev: setup
	@echo "Installing development dependencies..."
	$(BIN)/pip install -r requirements.txt
	$(BIN)/pip install -r requirements-dev.txt

# ------------------------------------------------------------------------------
# Code Quality
# ------------------------------------------------------------------------------
isort:
	$(BIN)/isort $(PYTHON_DIRS)

format:
	$(BIN)/isort $(PYTHON_DIRS)
	$(BIN)/black $(PYTHON_DIRS)

lint:
	$(BIN)/flake8 $(PYTHON_DIRS)
	$(BIN)/mypy $(PYTHON_DIRS)

check:
	$(MAKE) format
	$(MAKE) lint

# ------------------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------------------
test:
	@echo "Running all tests with coverage..."
	PYTHON_ENV=test $(BIN)/pytest --cov=. --cov-report=term-missing --cov-report=xml

# ------------------------------------------------------------------------------
# Utility
# ------------------------------------------------------------------------------
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info .pytest_cache .coverage coverage.xml htmlcov/ .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# ------------------------------------------------------------------------------
# Help
# ------------------------------------------------------------------------------
help:
	@echo "Available commands:"
	@echo "  make setup        - Create a virtual environment"
	@echo "  make install      - Install production requirements"
	@echo "  make install-dev  - Install dev + prod requirements"
	@echo "  make isort        - Sort imports"
	@echo "  make format       - Format code (isort + black)"
	@echo "  make lint         - Run flake8 + mypy"
	@echo "  make check        - Format + Lint"
	@echo "  make test         - Run pytest with coverage"
	@echo "  make clean        - Clean all build/cache artifacts"
