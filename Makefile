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
	@$(VENV)/bin/python main.py --suite all

test-ui: setup
	@$(VENV)/bin/python main.py --suite ui

test-responses: setup
	@$(VENV)/bin/python main.py --suite responses

test-parallel: setup
	@$(VENV)/bin/python main.py --parallel 3

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
	@echo "  make test-ui       - Run UI tests only"
	@echo "  make test-responses - Run response tests only"
	@echo "  make test-parallel - Run tests in parallel"
	@echo "  make clean         - Clean up the environment"
