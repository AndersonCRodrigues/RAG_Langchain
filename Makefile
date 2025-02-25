# Configurações
IMAGE_NAME=flask-gunicorn-app
PORT ?= 5000
ENV_FILE=.env
VENV=.venv

requirements:
	@pip freeze > requirements.txt

install:
	@python3.11 -m venv $(VENV)
	@$(VENV)/bin/pip install -r requirements.txt

activate:
	@echo "Execute: source $(VENV)/bin/activate"

mongo:
	@docker run -d -p 27017:27017 \
	  --name mongo-container \
	  -e MONGO_INITDB_ROOT_USERNAME=admin \
	  -e MONGO_INITDB_ROOT_PASSWORD=password \
	  mongo

wsgi:
	@$(VENV)/bin/gunicorn wsgi:app --bind 0.0.0.0:$(PORT)

dev:
	@$(VENV)/bin/python wsgi.py
