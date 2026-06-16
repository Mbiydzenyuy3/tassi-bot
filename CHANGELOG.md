# Changelog

All notable changes to this project will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Version bumps are managed by [commitizen](https://commitizen-tools.github.io/commitizen/) — run `make bump-version`.

## [Unreleased]

## [0.1.0] — 2026-06-16

### Added

- Repository scaffolding: `pyproject.toml`, uv lockfile, `.editorconfig`, `.gitignore`
- Minimal FastAPI application factory with `/health` liveness endpoint (`tassi/main.py`)
- Environment-driven configuration via pydantic-settings (`tassi/config.py`) — all tax rates, feature flags, and external credentials are config, not code (SRS NFR-MAINT-1)
- Test suite with 100% branch coverage on the initial skeleton (`tests/test_health.py`)
- Pre-commit hooks: Ruff (lint), Black (format), mypy (type-check), conventional-commit enforcement
- GitHub Actions CI/CD pipeline: lint → type-check → test → Docker build/push on main
- Dependabot for weekly updates (Python deps, GitHub Actions, Docker base images)
- Docker multi-stage build (builder + slim runtime, non-root user)
- `docker-compose.yml` for local dev stack (Postgres 17 + Redis 7 + app with hot-reload)
- `Makefile` with convenience targets for all common dev tasks
- Governing documentation: SRS v2.0, SDD v2.0, PERSONAS v2.0 (`docs/`)
