.DEFAULT_GOAL: help

help:
	@echo "Available commands:"
	@echo
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build:  ## Build docker image
	docker compose build

dev:  ## Start the development server on port 5000 and PostgresSQL container
	docker compose up -d && docker compose logs -f

api: ## Start the gunicorn server on port 5005 and the PostgreSQL db
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

dev-generator: ## Start the cap generator in dev mode
	docker compose -f docker-compose.cap_generator.yml up

generator:  ## Start the cap generator in production mode
	docker compose -f docker-compose.cap_generator.prod.yml up -d

down: ## Remove all containers
	docker compose down --remove-orphans

destroy: ## Remove all containers and images
	docker compose down --remove-orphans && docker image rm rss-api

restart:  ## Restart all containers
	docker compose restart

stop: ## Stop all containers
	docker compose stop

test:  ## Run all tests
	docker compose run --rm --no-deps --entrypoint=pytest rss-api /tests/

unit-tests: ## Run unit tests
	docker compose run --rm --no-deps --entrypoint=pytest rss-api /tests/unit

integration-tests: ## Run integration tests
	docker compose run --rm --no-deps --entrypoint=pytest rss-api /tests/integration

e2e-tests:  ## Run end to end test
	docker compose run --rm --no-deps --entrypoint=pytest rss-api /tests/e2e

logs:  ## View the logs
	docker compose logs --tail=25 rss-api
