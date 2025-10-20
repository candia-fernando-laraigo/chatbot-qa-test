# Simplified Chatbot QA Test Automation Makefile

# Variables
PYTHON = python3
VENV = venv
REQUIREMENTS = requirements.txt

.PHONY: all clean help report setup test test-examples 

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
    # Abrir el reporte HTML más reciente generado en reports/
	@if [ -d reports ] && ls reports/*.html >/dev/null 2>&1; then \
		latest_report=$$(ls -t reports/*.html | head -n 1); \
		echo "Abriendo $$latest_report"; \
		xdg-open "$$latest_report" 2>/dev/null || open "$$latest_report" 2>/dev/null || echo "Reporte generado en: $$latest_report"; \
	else \
		echo "No se encontraron reportes HTML en la carpeta reports/"; \
	fi

# Clean up
clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV) __pycache__ .pytest_cache
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete

# Help command
help:
	@printf "\nLaraigo Chatbot QA Automation\n"
	@printf "================================\n"
	@printf "\nUsage:\n  make <command>\n"
	@printf "\nCore Commands:\n"
	@printf "  %-16s %s\n" "setup" "Create/update venv and install requirements"
	@printf "  %-16s %s\n" "test" "Run default Laraigo suite via main.py"
	@printf "  %-16s %s\n" "test-examples" "Execute simple-web demo suite"
	@printf "  %-16s %s\n" "report" "Open the most recent HTML report"
	@printf "  %-16s %s\n" "clean" "Remove venv, caches, logs, screenshots"
	@printf "  %-16s %s\n" "help" "Display this command reference"
	@printf "\nDefault Usage:\n  make\n    - Creates the virtual environment and runs all tests in the laraigo suite\n"
	@printf "\nCommand Details:\n"
	@printf "  make setup\n    - Ensures the virtual environment exists\n    - Upgrades pip and installs requirements.txt\n\n"
	@printf "  make test\n    - Calls main.py with --suite laraigo\n\n"
	@printf "  make test-examples\n    - Runs the lightweight sandbox against simple-web/ for quick smoke checks\n\n"
	@printf "  make report\n    - Opens the newest file under reports/*.html (falls back to printing the path)\n\n"
	@printf "  make clean\n    - Deletes venv, __pycache__, .pytest_cache\n"
	@printf "\nEnvironment Notes:\n"
	@printf "  - Default browser: chrome headless (config/config.py)\n"
	@printf "  - Ensure Chrome/driver download allowed on first run\n"
	@printf "\nExamples:\n  make\n  make setup\n  make test\n  make report\n\n"


