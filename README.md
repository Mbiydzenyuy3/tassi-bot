# Tassi

[![CI](https://github.com/Mbiydzenyuy3/tassi-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/Mbiydzenyuy3/tassi-bot/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-≥99.98%25-brightgreen)](https://github.com/Mbiydzenyuy3/tassi-bot/actions)
[![Python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linting: ruff](https://img.shields.io/badge/linting-ruff-FCC21B.svg)](https://github.com/astral-sh/ruff)
[![Conventional Commits](https://img.shields.io/badge/commits-conventional-fe5196?logo=conventionalcommits)](https://www.conventionalcommits.org/)

**Tassi** is a WhatsApp bot that computes the monthly **Acompte** (advance tax) for Cameroonian SMEs under **Régime Simplifié d'Imposition (RSI)** — annual revenue 10M–50M XAF — with an optional paid tier for proactive reminders and filing history.

It runs entirely via WhatsApp (no app to install), is priced for small merchants, and is designed to be honest: it clearly labels what it's confident about and what still needs a tax advisor to confirm.

> **Status:** `main` is the project scaffold. Feature branches are where application code lives. See [CONTRIBUTING.md](CONTRIBUTING.md) for the branching strategy.

---

## Why Tassi?

Cameroonian SMEs face a monthly Acompte filing obligation they often miss — not from negligence, but because calculating it correctly and navigating the DGI Harmony portal is confusing. Most can't afford a tax consultant for a recurring calculation that's a simple percentage of monthly revenue.

Tassi sends a WhatsApp message, you reply with your monthly figure, and it replies with the math — in French or English, tolerating the messy number formats people actually type (`2.350.000 frs`, `2,350,000`, etc.).

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Web framework | FastAPI |
| Database | PostgreSQL 17 (SQLAlchemy + Alembic) |
| Cache / Session | Redis 7 |
| Messaging | Meta WhatsApp Business Cloud API |
| Payments | Campay (MTN MoMo + Orange Money) |
| Scheduler | APScheduler (in-process — no Celery) |
| Package manager | uv |
| CI/CD | GitHub Actions → GHCR → single EU VPS |

Full architecture rationale: [docs/SDD.md](docs/SDD.md)
Full requirements: [docs/SRS.md](docs/SRS.md)
User flows and "how it works": [docs/PERSONAS.md](docs/PERSONAS.md)

---

## Quick Start

### Prerequisites

- Python 3.12
- [uv](https://docs.astral.sh/uv/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Docker + Docker Compose

### Setup

```bash
git clone git@github.com:Mbiydzenyuy3/tassi-bot.git
cd tassi-bot
cp .env.example .env       # fill in Meta, Campay, DB credentials
make setup                 # uv sync --all-groups + install pre-commit hooks
```

### Run locally

```bash
# Start Postgres + Redis in the background
docker compose up postgres redis -d

# Apply migrations (first run)
make migrate

# Run the app with hot-reload
uv run uvicorn tassi.main:app --reload --port 8000
```

Or run the full stack (app + DB + Redis) in containers:

```bash
make docker-up     # background
make docker-logs   # follow app logs
```

Health check: `curl http://localhost:8000/health`

---

## Project Structure

```
tassi-bot/
├── tassi/                  # Application package (SDD §4)
│   ├── __init__.py         # __version__
│   ├── main.py             # FastAPI app factory
│   └── config.py           # pydantic-settings (all config is env-driven)
├── tests/
│   ├── conftest.py         # shared fixtures
│   └── test_health.py      # health endpoint + app factory tests
├── migrations/             # Alembic (auto-generated migration scripts)
├── docs/
│   ├── SRS.md              # Requirements v2.0
│   ├── SDD.md              # Design v2.0
│   └── PERSONAS.md         # User stories and "how it works"
├── .github/
│   ├── workflows/ci.yml    # lint → type-check → test → docker build/push
│   └── dependabot.yml
├── Dockerfile              # Multi-stage, non-root, production-ready
├── docker-compose.yml      # Local dev stack (Postgres + Redis + app)
├── pyproject.toml          # All project + tool config
├── uv.lock                 # Pinned dependency lockfile
└── Makefile                # Dev convenience targets (run `make help`)
```

Modules added by feature branches (not present yet):

```
tassi/
├── db.py          # SQLAlchemy engine/session
├── models.py      # users, tax_calculations, subscriptions, payment_transactions
├── chat.py        # WhatsApp webhook handler + Redis session state
├── tax.py         # RSI Acompte calculation engine (Decimal only, config-driven)
├── payments.py    # Campay integration + subscription logic
└── reminders.py   # APScheduler daily reminder job
```

---

## Development Commands

```bash
make help          # full list with descriptions
make check         # ruff + black --check + mypy (read-only)
make fix           # ruff --fix + black (auto-format)
make test          # pytest with ≥99.98% branch coverage
make test-fast     # pytest without coverage (quick feedback)
make coverage-html # open htmlcov/index.html in browser
make migrate       # alembic upgrade head
make migration MSG="add payments table"  # new autogenerated migration
```

---

## Testing

Tests use **pytest + pytest-cov** and must maintain **≥ 99.98% branch coverage**. The CI pipeline enforces this on every PR.

```bash
make test
```

**Financial math** (`tax.py`, when it exists) has dedicated rounding tests — every calculation function must have a fixture that tests the exact Decimal output, not just "it returns something." See `tests/test_tax.py` once that module is built.

---

## Architecture Notes

### CAP Theorem

The database (single Postgres node) is not distributed — CAP doesn't apply to it. The two places where real network partitions happen — and where the AP pattern is explicitly applied — are:

- **Meta → webhook**: duplicate delivery is routine on Cameroonian mobile networks; handled by Redis `SETNX` idempotency on `message_id` (SRS FR-CHAT-6)
- **Campay payment flow**: the success webhook may not arrive after PIN approval; handled by a `STATUS` command that polls Campay directly (SRS FR-PAY-4)

Full reasoning: [docs/SDD.md §3](docs/SDD.md#3-cap-theorem--applied-honestly)

### Validation Gates

Three open questions gate specific features. **Don't write code that assumes a gate is closed:**

| Gate | Question | Blocks |
|---|---|---|
| **G1** | Is CAC additive (+10% on Acompte) or already included in the 5.5%? | Showing a single combined total |
| **G2** | Does selling "Tassi Plus" require a fiscal-advisory license? | Guarantee-style marketing language |
| **G3** | Will users pay for Tassi Plus, and at what price? | Real price, enabling Day-10 reminders |

---

## Deployment

Single EU VPS (e.g. Hetzner CX21), Docker Compose, nightly `pg_dump` to object storage.

On every push to `main`, CI builds and pushes a Docker image to `ghcr.io/Mbiydzenyuy3/tassi-bot`. To wire up automatic deployment, uncomment the `deploy` job in [`.github/workflows/ci.yml`](.github/workflows/ci.yml) and add `VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY` as repository secrets.

**Code freeze: 8th–16th of each month** (SRS NFR-AVAIL-2) — no deploys during the filing window.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for branching strategy, commit message format (Conventional Commits), code quality standards, and the filing-window freeze policy.
