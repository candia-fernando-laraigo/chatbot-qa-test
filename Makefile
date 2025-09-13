# Simplified Chatbot QA Test Automation Makefile

# Variables
PYTHON = python3
VENV = venv
REQUIREMENTS = requirements.txt

.PHONY: all setup clean test help

all: setup test

# Setup virtual environment and install dependencies
setup:
	@if [ ! -d $(VENV) ]; then $(PYTHON) -m venv $(VENV); fi
	@echo "Setting up the test environment..."
	@$(VENV)/bin/pip install --upgrade pip
	@$(VENV)/bin/pip install -r $(REQUIREMENTS)

# Run tests with different options
test: setup
	@echo "Running all tests..."
	@$(VENV)/bin/python main.py --suite laraigo

test-examples: setup
	@$(VENV)/bin/python main.py --suite examples

report:
	# Detectar y abrir el reporte HTML generado
	@if [ -f report.html ]; then xdg-open report.html || open report.html; else echo "No report.html found!"; fi

# Clean up
clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV) __pycache__ .pytest_cache logs/*.log screenshots/*.png report.html
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete

# Help command
help:
	@echo "Available commands:"
	@echo "  make setup         - Set up the environment"
	@echo "  make test          - Run all tests"
	@echo "  make test-examples - Run example tests only"
	@echo "  make clean         - Clean up the environment"
