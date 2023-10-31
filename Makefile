.DEFAULT_GOAL: help

help:
	@echo "Available commands:"
	@echo
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build: ## Build the docker images
	docker compose build

dev:  ## Start the API, DB, client and cap generator in development mode.
	docker compose up -d && docker compose logs -f

prod: ## Start the API, DB, client and cap generator in production mode.
	docker compose -f docker-compose.prod.yml up

web-dev: ## Start the API, DB and client in dev mode. Does not start cap generator.
	docker compose up rss-api rss-client postgres

generator-dev: ## Start the cap generator in dev mode.
	docker compose up cap-generator alerts-service

generator:  ## Start the cap generator in production mode.
	docker compose up cap-generator alerts-service -f docker-compose.prod.yml

down: ## Remove all containers.
	docker compose down --remove-orphans

restart:  ## Restart all containers.
	docker compose restart

stop: ## Stop all containers.
	docker compose stop

api-test:  ## Run all api tests.
	docker compose run --rm --no-deps --entrypoint=pytest rss-api /tests/

api-unit-tests: ## Run unit tests.
	docker compose run --rm --no-deps --entrypoint=pytest rss-api /tests/unit

api-integration-tests: ## Run integration tests.
	docker compose run --rm --no-deps --entrypoint=pytest rss-api /tests/integration

seed-db:  ## Add multiple alerts to the database
	docker compose exec rss-api flask seed-db

logs:  ## View the logs.
	docker compose logs --tail=25 rss-api
