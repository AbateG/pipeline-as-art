.PHONY: up down ps logs curl health clean

up: ## Build and start the stack
	docker compose up -d --build

down: ## Stop and remove containers and volumes
	docker compose down -v

ps: ## Show container status
	docker compose ps

logs: ## Tail logs
	docker compose logs -f --tail=200

health: ## Quick health checks
	@echo "Gateway -> http://localhost/"; \
	curl -fsS http://localhost/ | sed -n '1,2p'; echo; \
	echo "API -> http://localhost/api/healthz"; \
	curl -fsS http://localhost/api/healthz; echo; \
	echo "About (ES) -> http://localhost/api/about?lang=es"; \
	curl -fsS "http://localhost/api/about?lang=es" | sed -n '1,2p'; echo

clean: ## Prune volumes
	docker volume rm pipeline-as-art_db-data pipeline-as-art_redis-data || true