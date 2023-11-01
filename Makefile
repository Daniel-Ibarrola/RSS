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

prod-web: ## Start the API, DB, and client in production mode.
	docker compose -f docker-compose.prod.yml up -d rss-api rss-client postgres

web-dev: ## Start the API, DB and client in dev mode. Does not start cap generator.
	docker compose up rss-api rss-client postgres

generator-dev: ## Start the cap generator in dev mode.
	docker compose up cap-generator alerts-service

generator:  ## Start the cap generator in production mode.
	docker compose -f docker-compose.prod.yml up -d cap-generator

down: ## Remove all containers.
	docker compose down --remove-orphans

restart:  ## Restart all containers.
	docker compose restart

stop: ## Stop all containers.
	docker compose stop

restore_db:  ## Restore the postgres database from a backup file (requires file and user args)
	docker cp $(file) rss-db:/$(file) && docker compose exec postgres pg_restore -U $(user) -d rss $(file)

seed-db:  ## Add multiple alerts to the database
	docker compose exec rss-api flask seed-db

ssl-certificate: ## Generate an ssl certificate for https. Must run with production config in server
	docker compose -f docker-compose.prod.yml run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d rss.sasmex.net

nginx-https: ## Update nginx config to accept https requests after obtaining and ssl certificate
	cp services/client/nginx/rss.sasmex.net.conf services/client/nginx/https.conf && docker compose -f docker-compose.prod.yml restart

logs:  ## View the logs.
	docker compose logs --tail=25

api-test:  ## Run all api tests.
	docker compose run --rm --no-deps --entrypoint=pytest rss-api /tests/

api-unit-tests: ## Run unit tests.
	docker compose run --rm --no-deps --entrypoint=pytest rss-api /tests/unit

api-integration-tests: ## Run integration tests.
	docker compose run --rm --no-deps --entrypoint=pytest rss-api /tests/integration

client-tests: ## Run client unit tests
	docker compose exec rssc-client npm run test

cap-gen-test: ## Run cap-gen unit tests
	docker compose run --rm --no-deps --entrypoint=pytest cap-generator /tests/unit
