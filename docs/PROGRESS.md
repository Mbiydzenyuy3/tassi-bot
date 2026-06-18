# Tassi MVP — Build Progress

**Governing document:** `docs/TASKS.md`
**Rule:** Update this file every time a task or milestone is marked complete. Status must match git history — do not mark complete until `make test` passes and the commit is on the branch.

---

## Status Legend

- `[x]` Complete — tests green, committed
- `[~]` In progress
- `[ ]` Not started

---

## Pre-Task Scaffold (already done at project start)

| Item | Status |
|---|---|
| Repo scaffold: `pyproject.toml`, `Dockerfile`, `docker-compose.yml`, `Makefile`, `CHANGELOG.md` | `[x]` |
| Pre-commit hooks: Ruff, Black, detect-private-key, commitizen commit-msg | `[x]` |
| GitHub Actions CI: lint → type-check → test → Docker build/push | `[x]` |
| `tassi/__init__.py` — version string `"0.1.0"` | `[x]` |
| `tassi/config.py` — pydantic-settings, env-driven tax rates, feature flags | `[x]` |
| `tassi/main.py` — `create_app(settings)` factory, `/health` endpoint | `[x]` |
| `tests/conftest.py` — `settings`, `client`, `client_production` fixtures | `[x]` |
| `tests/test_health.py` — 16 tests, 100% branch coverage (updated through Task 1.4) | `[x]` |
| `migrations/env.py` — reads `DATABASE_URL` from environment | `[x]` |
| `.env.example` — all required variables with placeholder values | `[x]` |
| `.gitignore` | `[x]` |

---

## Milestone 1 — Database Layer

**Goal:** Four tables defined, migrated, and tested. No application logic yet.

| Task | Description | Branch | Status | Notes |
|---|---|---|---|---|
| 1.1 | `tassi/db.py` — engine, session factory, `get_db_session` | `feat/database-layer` | `[x]` | Merged to `main` via PR. 14 tests, 100% coverage. |
| 1.2 | `tassi/models.py` — four ORM models | `feat/models` | `[x]` | Merged to `development` via PR (hash a288bf1). 30 tests at time of merge, 100% coverage. `language` column widened to `String(3)` for fr/en/pcm. |
| 1.3 | Alembic initial migration | `feat/alembic-migration` | `[x]` | Merged to `development` via PR. Manual migration (no live Postgres for autogenerate); verified clean via `alembic upgrade head --sql` offline SQL. All 4 tables, FK constraints, `ix_tax_calculations_user_period` index, `downgrade()` in reverse FK order. `make test` still passes. |
| 1.4 | Wire `db.py` into `main.py` lifespan | `feat/wire-db` | `[x]` | Merged to `development` via PR #10. `asynccontextmanager` lifespan: builds engine + session factory on startup, stores both on `app.state`, disposes engine on shutdown. No `create_all` (Alembic-only). 4 new `TestLifespan` tests. Total: 62 tests, 100% branch coverage. |

---

## Milestone 2 — Tax Calculation Engine

**Goal:** Pure calculation functions, fully tested, zero I/O.

| Task | Description | Branch | Status | Notes |
|---|---|---|---|---|
| 2.1 | `parse_revenue(raw) -> Decimal \| None` | `feat/tax-engine` | `[x]` | Handles 9 input formats: plain int, spaces, dot/comma thousands, decimal, XAF/frs/fcfa suffixes, negatives. |
| 2.2 | `is_zero_return(raw) -> bool` (incl. Pidgin phrases per SRS FR-TAX-3) | `feat/tax-engine` | `[x]` | French: rien, néant, neant. English: nothing, nada. Pidgin: e no get, no money, e finish, nothing dey, i no sell. Numeric zeros via parse_revenue. |
| 2.3 | `calculate_rsi(...)` → `TaxResult` dataclass | `feat/tax-engine` | `[x]` | All 7 spec test cases pass. ROUND_HALF_UP throughout. ADDITIVE/INCLUDED/UNCONFIRMED modes. cac_rate stored for formatter. |
| 2.4 | `format_tax_result(result, language) -> str` | `feat/tax-engine` | `[x]` | Trilingual: fr/en/pcm. All 3 cac_modes. Unknown language falls back to fr. |
| 2.5 | `tests/test_tax.py` — exhaustive tests for all above | `feat/tax-engine` | `[x]` | 82 tests. 100% branch coverage on tax.py. No float in tax.py. Awaiting commit + push. |

---

## Milestone 3 — Webhook Ingestion

**Goal:** Tassi can receive a WhatsApp message, acknowledge it in <500ms, and not process duplicates.

| Task | Description | Branch | Status | Notes |
|---|---|---|---|---|
| 3.1 | Meta webhook verification endpoint (`GET /webhook`) | `feat/webhook` | `[x]` | Token match + challenge echo. 3 tests. |
| 3.2 | `tassi/security.py` — Meta signature verification (HMAC) | `feat/webhook` | `[x]` | `hmac.compare_digest`, timing-safe, never raises. 4 tests. |
| 3.3 | Webhook POST endpoint + background task dispatch | `feat/webhook` | `[x]` | Acks <500ms, HMAC check, idempotency, rate limit, BackgroundTasks dispatch. 5 tests. |
| 3.4 | `tassi/session.py` — Redis session, dedup, rate limit | `feat/webhook` | `[x]` | 5 async functions, full RedisError degraded-mode coverage. Real Redis tests. 14 tests. |
| 3.5 | `tassi/deps.py` — FastAPI Redis + DB dependencies | `feat/webhook` | `[x]` | `get_cfg`, `get_redis`, `get_db` — used via `Depends()` in routes. 3 tests. |

---

## Milestone 4 — Conversation Flow

**Goal:** Full onboarding → revenue input → calculation reply. Both languages. PERSONAS T1–T6 all pass.

| Task | Description | Branch | Status | Notes |
|---|---|---|---|---|
| 4.1 | `tassi/templates.py` — all bot message text (fr + en) | `feat/conversation` | `[ ]` | |
| 4.2 | `tassi/chat.py` — state machine + per-message language detection (FR-CHAT-7) | `feat/conversation` | `[ ]` | Uses langdetect; falls back to users.language for numeric input |
| 4.3 | `tassi/meta.py` — `send_typing_indicator()` + `send_text_message()` (FR-CHAT-8) | `feat/conversation` | `[ ]` | Typing indicator is best-effort, never blocks reply |
| 4.4 | `tests/test_conversation.py` — integration tests T1–T6 + language-switch + typing indicator | `feat/conversation` | `[ ]` | |

---

## Milestone 5 — Payments & Subscriptions

**Gate: G2 must close before going live in production.**

| Task | Description | Branch | Status | Notes |
|---|---|---|---|---|
| 5.1 | `tassi/campay.py` — Campay API client | `feat/payments` | `[ ]` | |
| 5.2 | SUBSCRIBE command handler | `feat/payments` | `[ ]` | |
| 5.3 | Campay webhook callback (`POST /campay/webhook`) + `tassi/payments.py` | `feat/payments` | `[ ]` | |
| 5.4 | STATUS command handler | `feat/payments` | `[ ]` | |
| 5.5 | HISTORY command handler | `feat/payments` | `[ ]` | |
| 5.6 | `tests/test_payments.py` — integration tests T7–T10 | `feat/payments` | `[ ]` | |

---

## Milestone 6 — Notifications & Reminders

**Goal:** Automated filing reminders and renewal prompts. Day-10 flag stays off until G3 closes.

| Task | Description | Branch | Status | Notes |
|---|---|---|---|---|
| 6.1 | APScheduler setup in FastAPI lifespan | `feat/reminders` | `[ ]` | |
| 6.2 | `send_day_14_reminders()` | `feat/reminders` | `[ ]` | |
| 6.3 | `send_day_10_reminders()` (feature-flagged off) | `feat/reminders` | `[ ]` | |
| 6.4 | `send_renewal_prompts()` | `feat/reminders` | `[ ]` | |
| 6.5 | `daily_reminder_job()` wrapper | `feat/reminders` | `[ ]` | |
| 6.6 | `tests/test_reminders.py` — T11–T13 + idempotency tests | `feat/reminders` | `[ ]` | |

---

## Milestone 7 — Production Deployment

**Goal:** Running on real VPS, Meta webhook registered, nightly backup, uptime monitor.

| Task | Description | Status | Notes |
|---|---|---|---|
| 7.1 | VPS provisioning (Hetzner CX21) | `[ ]` | |
| 7.2 | `docker-compose.prod.yml` | `[ ]` | |
| 7.3 | Production `.env` on VPS | `[ ]` | |
| 7.4 | Nightly backup + restore drill | `[ ]` | |
| 7.5 | UptimeRobot monitoring | `[ ]` | |
| 7.6 | Meta webhook registration | `[ ]` | |
| 7.7 | Campay production credentials | `[ ]` | |

---

## Milestone 8 — Acceptance Testing

**Goal:** All 17 PERSONAS test scenarios pass in production.

| Scenario | Description | Status |
|---|---|---|
| T1 | Standard calculation — French | `[ ]` |
| T2 | Standard calculation — English | `[ ]` |
| T3 | Déclaration Néant | `[ ]` |
| T4 | Invalid input recovery | `[ ]` |
| T5 | Duplicate message delivery | `[ ]` |
| T6 | RESEND command | `[ ]` |
| T7 | MTN MoMo subscription success | `[ ]` |
| T8 | Dropped webhook + STATUS recovery | `[ ]` |
| T9 | Duplicate Campay callback | `[ ]` |
| T10 | Failed payment | `[ ]` |
| T11 | Day-14 reminder | `[ ]` |
| T12 | Day-10 reminder (flag off) | `[ ]` |
| T13 | Renewal prompt | `[ ]` |
| T14 | Revenue band rejection | `[ ]` |
| T15 | Redis-down degraded mode | `[ ]` |
| T16 | Rounding correctness | `[ ]` |
| T17 | Config-driven rate change without deployment | `[ ]` |

---

## Milestone 9 — Wizard-of-Oz Pilot (Gate G3)

**Goal:** Validate paying demand and set a real price for Tassi Plus.

| Task | Status | Notes |
|---|---|---|
| Recruit 20–30 RSI SME business owners | `[ ]` | |
| Run one complete filing cycle | `[ ]` | |
| Collect willingness-to-pay data | `[ ]` | |
| Close Gate G3 in SRS §3 with date and validated price | `[ ]` | |

---

## Open Validation Gates

| Gate | Status | Blocks |
|---|---|---|
| G1 — CAC additive or included? | **OPEN** | `cac_mode` config, showing combined total |
| G2 — Fiscal advisory license needed? | **OPEN** | Going live with real charges |
| G3 — Users will pay for Plus at what price? | **OPEN** | Real price, Day-10 reminders |
