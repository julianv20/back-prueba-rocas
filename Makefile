.PHONY: install run test clean docker-build docker-up docker-down format lint

# Install dependencies
install:
	pip install -r requirements.txt

# Run the application
run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
test:
	pytest -v --cov=app tests/

# Run tests with coverage report
test-cov:
	pytest -v --cov=app --cov-report=html tests/

# Clean cache and temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete

# Docker commands
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Code formatting
format:
	black app/ tests/
	ruff check --fix app/ tests/

# Linting
lint:
	black --check app/ tests/
	ruff check app/ tests/
	mypy app/

# Database migrations
migrate:
	alembic upgrade head

# Create new migration
migration:
	alembic revision --autogenerate -m "$(msg)"

# Development setup
dev-setup: install
	cp .env.example .env
	@echo "Development environment ready!"
	@echo "Don't forget to update .env with your settings"
