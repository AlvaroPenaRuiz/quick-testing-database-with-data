.PHONY: up down build logs ps reset health

# ── Local / dev ───────────────────────────────────────────────────────────────

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

ps:
	docker compose ps

# ── Production (Traefik) ──────────────────────────────────────────────────────

prod-up:
	docker compose -f docker-compose.prod.yml up -d

prod-down:
	docker compose -f docker-compose.prod.yml down

prod-build:
	docker compose -f docker-compose.prod.yml build

prod-logs:
	docker compose -f docker-compose.prod.yml logs -f

prod-ps:
	docker compose -f docker-compose.prod.yml ps

# ── DB helpers ────────────────────────────────────────────────────────────────

health:
	curl -s http://localhost:8081/health | python3 -m json.tool

reset:
	curl -s -X POST http://localhost:8081/reset \
		-H "X-Reset-Token: $${RESET_TOKEN:-changeme}" | python3 -m json.tool
