.PHONY: help install dev test lint format clean docker-build docker-up docker-down

help:
	@echo "CyberTrap-AI Development Commands"
	@echo "==================================="
	@echo "make install      - Install dependencies"
	@echo "make dev         - Run development server"
	@echo "make test        - Run tests"
	@echo "make test-cov    - Run tests with coverage"
	@echo "make lint        - Run linting checks"
	@echo "make format      - Format code with black"
	@echo "make clean       - Clean temporary files"
	@echo "make db-init     - Initialize database"
	@echo "make db-migrate  - Run database migrations"
	@echo "make docker-build - Build Docker image"
	@echo "make docker-up   - Start Docker containers"
	@echo "make docker-down - Stop Docker containers"

install:
	pip install -r requirements.txt

dev:
	flask run --debug

test:
	pytest

test-cov:
	pytest --cov=app --cov-report=html

lint:
	flake8 app tests
	pylint app

format:
	black app tests
	isort app tests

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

db-init:
	python scripts/init_db.py

db-migrate:
	flask db upgrade

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down
