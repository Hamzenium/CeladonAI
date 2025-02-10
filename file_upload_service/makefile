# Makefile

# Variables
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

# Targets

.PHONY: help install run test clean

help:
	@echo "Available targets:"
	@echo "  make install      - Set up the virtual environment and install dependencies"
	@echo "  make run          - Run the Flask application"
	@echo "  make test         - Run tests using pytest"
	@echo "  make clean        - Remove virtual environment and temporary files"

build:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	FLASK_APP=app.py FLASK_ENV=development $(PYTHON) -m flask run

test:
	$(PYTHON) -m pytest

clean:
	rm -rf $(VENV_DIR)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
