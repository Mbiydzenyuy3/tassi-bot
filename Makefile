.DEFAULT_GOAL := help

# ── Dev environment ────────────────────────────────────────────────────────────
install: ## Install all dependencies (requires uv)
	uv sync --all-groups

install-hooks: ## Install pre-commit hooks (pre-commit + commit-msg stages)
	uv run pre-commit install --hook-type pre-commit --hook-type commit-msg

setup: install install-hooks ## Full one-shot dev environment setup

# ── Code quality ───────────────────────────────────────────────────────────────
lint: ## Run Ruff linter
	uv run ruff check .

lint-fix: ## Run Ruff and auto-fix safe issues
	uv run ruff check . --fix

fmt: ## Format code with Black
	uv run black .

fmt-check: ## Check formatting without making changes
	uv run black --check .

type-check: ## Run mypy strict type checking
	uv run mypy tassi

check: lint fmt-check type-check ## Run all static checks (read-only, no auto-fix)

fix: lint-fix fmt ## Auto-fix lint issues and format code

# ── Testing ────────────────────────────────────────────────────────────────────
test: ## Run tests with branch coverage (fails below 99.98%)
	uv run pytest

test-fast: ## Run tests without coverage reporting
	uv run pytest --no-cov -q

test-watch: ## Run tests in watch mode (requires pytest-watch)
	uv run ptw -- --no-cov -q

coverage-html: ## Generate HTML coverage report, then open it
	uv run pytest --cov-report=html --no-cov-on-fail
	@echo "Open htmlcov/index.html to view the report."

# ── Database migrations ────────────────────────────────────────────────────────
migrate: ## Apply all pending Alembic migrations
	uv run alembic upgrade head

migrate-down: ## Roll back the last Alembic migration
	uv run alembic downgrade -1

migration: ## Create a new migration — usage: make migration MSG="add users table"
	@test -n "$(MSG)" || (echo "Usage: make migration MSG=\"description\"" && exit 1)
	uv run alembic revision --autogenerate -m "$(MSG)"

migrate-history: ## Show migration history
	uv run alembic history --verbose

# ── Docker ─────────────────────────────────────────────────────────────────────
docker-build: ## Build the production Docker image
	docker build -t tassi-bot:local .

docker-up: ## Start the local stack (Postgres + Redis + app) in the background
	docker compose up -d

docker-down: ## Stop and remove local stack containers
	docker compose down

docker-logs: ## Tail app container logs
	docker compose logs -f app

docker-shell: ## Open a shell in the running app container
	docker compose exec app /bin/sh

# ── Utilities ──────────────────────────────────────────────────────────────────
clean: ## Remove all build/test/cache artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage coverage.xml htmlcov/ .pytest_cache/ .mypy_cache/ .ruff_cache/ dist/ build/

update-hooks: ## Update all pre-commit hooks to latest versions
	uv run pre-commit autoupdate

bump-version: ## Bump project version following Conventional Commits (uses commitizen)
	uv run cz bump

changelog: ## Preview the next CHANGELOG entry
	uv run cz changelog --dry-run

help: ## Show this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\n\033[1mUsage:\033[0m\n  make \033[36m<target>\033[0m\n\n\033[1mTargets:\033[0m\n"} \
	/^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

.PHONY: install install-hooks setup lint lint-fix fmt fmt-check type-check check fix \
        test test-fast test-watch coverage-html migrate migrate-down migration \
        migrate-history docker-build docker-up docker-down docker-logs docker-shell \
        clean update-hooks bump-version changelog help
