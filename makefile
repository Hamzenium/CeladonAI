# Makefile for Flask Application

# Variables
PYTHON = python
VENV_DIR = venv

# Target
.PHONY: run

run:
	@echo "Running Flask application..."
	@if [ -d "$(VENV_DIR)" ]; then \
		$(VENV_DIR)/bin/python app.py; \
	else \
		$(PYTHON) -m venv $(VENV_DIR) && \
		$(VENV_DIR)/bin/pip install -r requirements.txt && \
		$(VENV_DIR)/bin/python app.py; \
	fi
