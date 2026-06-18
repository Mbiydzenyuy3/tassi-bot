# Tassi MVP — Task Breakdown

**Governing documents:** SRS v2.0 · SDD v2.0 · PERSONAS v2.0
**Rule:** If a task cannot be traced to an FR, an NFR, or a PERSONAS test scenario, it does not belong here.

---

## Status Legend

- `[ ]` Not started
- `[x]` Complete — `make test` passes, coverage ≥ 99.98%
- `[~]` In progress

---

## What Is Already Done

These are complete and tested. Do not touch them unless a later task requires a change.

- [x] Repo scaffold: `pyproject.toml`, `Dockerfile`, `docker-compose.yml`, `Makefile`, `CHANGELOG.md`
- [x] Pre-commit hooks: Ruff, Black, detect-private-key, commitizen commit-msg
- [x] GitHub Actions CI: lint → type-check → test → Docker build/push
- [x] `tassi/__init__.py` — version string `"0.1.0"`
- [x] `tassi/config.py` — all settings via `pydantic-settings`, env-driven tax rates, feature flags
- [x] `tassi/main.py` — `create_app(settings)` factory, `/health` endpoint
- [x] `tests/conftest.py` — `settings`, `client`, `client_production` fixtures
- [x] `tests/test_health.py` — 12 tests, 100% branch coverage
- [x] `migrations/env.py` — reads `DATABASE_URL` from environment, no hardcoded credentials
- [x] `.env.example` — all required variables with placeholder values, safe to commit
- [x] `.gitignore` — `.env`, `*.pem`, `*.key`, `.claude/settings.json`, docs gitignored

---

## Milestone 1 — Database Layer

**Goal:** Four tables defined, migrated, and tested. No application logic yet.
**Branch:** `feat/database-layer`
**Commit prefix:** `feat(db):`

---

### Task 1.1 — Write `tassi/db.py`

**File:** `tassi/db.py` (new file)

Create the SQLAlchemy engine and session factory. Nothing else goes in this file.

```python
# What to implement:
engine: Engine           # created from Settings.database_url
AsyncSessionLocal: sessionmaker  # async session factory
Base: DeclarativeBase    # imported by models.py

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    # FastAPI dependency: yields a session, rolls back on error, closes always
    ...
```

**Python rules for this file:**
- Use SQLAlchemy 2.0 async API: `create_async_engine`, `AsyncSession`, `async_sessionmaker`
- The engine must be created lazily (inside a function), not at module import time — module-level engine creation breaks tests that need different DATABASE_URL values
- `get_db` must use `try / finally` — not `contextlib.asynccontextmanager` — so rollback on exception is explicit and visible

**Tests:** `tests/test_db.py`
- `test_get_db_yields_session` — verify `get_db()` yields an `AsyncSession`
- `test_get_db_closes_on_exit` — verify the session is closed after the generator is exhausted
- No actual DB connection required for these tests — mock the engine

**Done when:** `make test` passes. `mypy tassi/db.py` reports no errors.

---

### Task 1.2 — Write `tassi/models.py`

**File:** `tassi/models.py` (new file)

Four models exactly as specified in SDD §5. Copy the column names, types, and constraints from the SDD precisely — do not improvise.

```python
# Models to implement:
class User(Base): ...
class TaxCalculation(Base): ...
class Subscription(Base): ...
class PaymentTransaction(Base): ...
```

**Column-by-column requirements (SDD §5):**

`users`:
- `id: Mapped[uuid.UUID]` — primary key, `default=uuid.uuid4`
- `whatsapp_id: Mapped[str]` — unique, not null (the MSISDN)
- `language: Mapped[str]` — `"fr"` or `"en"`, default `"fr"`
- `annual_revenue_band: Mapped[str | None]` — nullable until onboarding complete
- `created_at: Mapped[datetime]` — `server_default=func.now()`
- `updated_at: Mapped[datetime]` — `onupdate=func.now()`
- **No `is_plus` column** — Plus status is always derived live from `subscriptions` (see APP.md §4.2 data integrity note)
- Property `is_plus(self) -> bool` — queries `subscriptions` for active row with `period_end > now()`. This is a Python property, not a DB column.

`tax_calculations`:
- `id: Mapped[uuid.UUID]` — primary key
- `user_id: Mapped[uuid.UUID]` — FK → `users.id`, not null
- `fiscal_period: Mapped[str]` — `"YYYY-MM"` format, not null
- `gross_revenue: Mapped[Decimal]` — `Numeric(precision=15, scale=2)`, not null
- `base_acompte: Mapped[Decimal]` — `Numeric(precision=15, scale=2)`, not null
- `cac_amount: Mapped[Decimal | None]` — nullable (null when `cac_mode=UNCONFIRMED`)
- `cac_mode: Mapped[str]` — `"ADDITIVE"`, `"INCLUDED"`, or `"UNCONFIRMED"`
- `is_zero_return: Mapped[bool]` — default `False`
- `created_at: Mapped[datetime]` — `server_default=func.now()`
- Composite index on `(user_id, fiscal_period)`
- **No UPDATE, no DELETE** — this table is append-only. Enforce via SQLAlchemy events if desired, but minimum: document it clearly in a comment on the model.

`subscriptions`:
- `id: Mapped[uuid.UUID]` — primary key
- `user_id: Mapped[uuid.UUID]` — FK → `users.id`, not null
- `status: Mapped[str]` — `"ACTIVE"` or `"EXPIRED"` or `"CANCELLED"`
- `period_start: Mapped[datetime]` — not null
- `period_end: Mapped[datetime]` — not null
- `price_xaf: Mapped[int]` — XAF amount paid (integer — XAF has no subunits)
- `created_at: Mapped[datetime]` — `server_default=func.now()`

`payment_transactions`:
- `id: Mapped[uuid.UUID]` — primary key
- `user_id: Mapped[uuid.UUID]` — FK → `users.id`, not null
- `subscription_id: Mapped[uuid.UUID | None]` — FK → `subscriptions.id`, nullable (transaction exists before subscription is activated)
- `campay_reference: Mapped[str | None]` — Campay's transaction ID, nullable until returned
- `operator: Mapped[str]` — `"MTN"` or `"ORANGE"`
- `amount_xaf: Mapped[int]` — not null
- `status: Mapped[str]` — `"PENDING"`, `"SUCCESS"`, `"FAILED"`
- `created_at: Mapped[datetime]` — `server_default=func.now()`
- `updated_at: Mapped[datetime]` — `onupdate=func.now()`

**Python rules for this file:**
- Use SQLAlchemy 2.0 mapped column syntax: `Mapped[type]` + `mapped_column()`, not the old `Column()` style
- Import `Decimal` from `decimal`, not Python builtins
- All `Numeric` columns must use `asdecimal=True` (the default) — never `Float`
- Every model must have `__tablename__` and `__repr__` (one-line, shows id and key field)

**Tests:** `tests/test_models.py`
- `test_user_repr` — `repr(user)` contains the whatsapp_id
- `test_user_is_plus_false_when_no_subscription` — property returns `False` with no rows
- `test_user_is_plus_false_when_subscription_expired` — property returns `False` when `period_end < now()`
- `test_user_is_plus_true_when_active_subscription` — property returns `True` when active
- `test_tax_calculation_uses_decimal` — `gross_revenue` is `Decimal`, not `float`
- `test_payment_transaction_statuses` — all three status values are valid strings

**Done when:** `make test` passes. No `Float` type anywhere in `models.py`.

---

### Task 1.3 — Write Initial Alembic Migration

**File:** `migrations/versions/0001_initial_schema.py` (generated, then edited)

```bash
# Generate the migration:
uv run alembic revision --autogenerate -m "initial schema"
```

Then read the generated file and verify:
- All four tables are created
- The `(user_id, fiscal_period)` index on `tax_calculations` is present
- `Numeric(15, 2)` columns are correct (autogenerate sometimes chooses wrong precision)
- FK constraints are present
- No `is_plus` column exists in `users`

If autogenerate missed anything, add it manually to `upgrade()`.

Always write `downgrade()` — it must `drop_table` in reverse order (respecting FK dependencies).

**Done when:** `make migrate` runs cleanly on a fresh Postgres instance. `make test` still passes.

---

### Task 1.4 — Wire `db.py` into `main.py`

**File:** `tassi/main.py` (edit existing)

Attach the database engine lifecycle to the FastAPI app:

```python
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # startup: create tables if in test/dev mode
    # (production uses alembic migrations — never create_all in production)
    yield
    # shutdown: dispose engine

app = FastAPI(..., lifespan=lifespan)
```

In tests, the `client` fixture already provides an override for `DATABASE_URL`. This task just ensures the app starts and stops cleanly.

**Done when:** `make test` passes. Starting the app locally (`make dev`) does not crash on import.

---

**Milestone 1 commit:**
```
feat(db): add SQLAlchemy models, session factory, and initial migration
```

---

## Milestone 2 — Tax Calculation Engine

**Goal:** Pure calculation functions, fully tested, zero I/O. This module has no knowledge of HTTP, databases, or WhatsApp.
**Branch:** `feat/tax-engine`
**Commit prefix:** `feat(tax):`

**The most important rule for this milestone:** Every function in `tax.py` must be a pure function. No database calls. No Redis calls. No HTTP. Input goes in, output comes out. This makes it trivially testable and independently auditable.

---

### Task 2.1 — Write `parse_revenue(raw: str) -> Decimal | None`

**File:** `tassi/tax.py` (new file)

Parse messy user input into a clean `Decimal`. This is the function that handles NFR-USE-2 (forgiving input).

```python
def parse_revenue(raw: str) -> Decimal | None:
    """
    Convert user-entered revenue string to Decimal.
    Returns None if the string cannot be parsed as a positive number.
    """
```

**Must handle all of these correctly (from PERSONAS edge case E3):**

| Input | Expected output |
|---|---|
| `"2350000"` | `Decimal("2350000")` |
| `"2 350 000"` | `Decimal("2350000")` |
| `"2.350.000"` | `Decimal("2350000")` |
| `"2,350,000"` | `Decimal("2350000")` |
| `"2350000 frs"` | `Decimal("2350000")` |
| `"2 350 000 XAF"` | `Decimal("2350000")` |
| `"2350000.00"` | `Decimal("2350000.00")` |
| `"1,500,000.50"` | `Decimal("1500000.50")` |
| `"abc"` | `None` |
| `""` | `None` |
| `"-1000"` | `None` (negative revenue is not valid) |
| `"0"` | `Decimal("0")` (valid — zero revenue is the Néant path) |

**Strategy:** Strip all whitespace, strip known currency suffixes (`frs`, `xaf`, `fcfa` case-insensitive), then try to detect whether `.` or `,` is a decimal separator or a thousands separator based on context. Use `re` for this — not `float()`, never `float()`.

---

### Task 2.2 — Write `is_zero_return(raw: str) -> bool`

**File:** `tassi/tax.py` (same file, new function)

```python
def is_zero_return(raw: str) -> bool:
    """
    Return True if the user's input indicates zero revenue this period.
    Handles: "0", "rien", "néant", "nothing", "0.00", "0 frs", etc.
    """
```

**Must return `True` for (from PERSONAS edge case E5):**
- `"0"`, `"0.00"`, `"0 frs"`, `"0 XAF"`
- `"rien"`, `"Rien"`, `"RIEN"`
- `"néant"`, `"Néant"`, `"neant"`
- `"nothing"`, `"Nothing"`
- `"nada"`

**Must return `False` for:**
- Any string that `parse_revenue()` would parse as a positive number
- `"abc"` (unparseable, not a zero declaration)

---

### Task 2.3 — Write `calculate_rsi(...)` — the core engine

**File:** `tassi/tax.py` (same file, new function)

```python
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

@dataclass(frozen=True)
class TaxResult:
    gross_revenue: Decimal
    base_acompte: Decimal
    cac_amount: Decimal | None  # None when cac_mode is UNCONFIRMED
    cac_mode: str               # "ADDITIVE" | "INCLUDED" | "UNCONFIRMED"
    total_due: Decimal | None   # None when cac_mode is UNCONFIRMED

def calculate_rsi(
    gross_revenue: Decimal,
    rate_rsi: Decimal,
    cac_mode: str,
    cac_rate: Decimal,
) -> TaxResult:
    """
    Calculate RSI Acompte for a given gross revenue.
    All arithmetic uses Decimal with ROUND_HALF_UP to 2 decimal places.
    """
```

**Arithmetic rules (SRS §2.3 and SDD §6):**

```
base_acompte = gross_revenue × rate_rsi  →  round to 2dp ROUND_HALF_UP

ADDITIVE mode:
    cac_amount = base_acompte × cac_rate  →  round to 2dp ROUND_HALF_UP
    total_due  = base_acompte + cac_amount

INCLUDED mode:
    cac_amount = Decimal("0.00")
    total_due  = base_acompte

UNCONFIRMED mode:
    cac_amount = None
    total_due  = None  (shown as unconfirmed to user)
```

**Non-negotiable test cases — every one must be a named test:**

| gross_revenue | rate_rsi | cac_mode | cac_rate | base_acompte | cac_amount | total_due |
|---|---|---|---|---|---|---|
| `2350000.00` | `0.055` | `UNCONFIRMED` | `0.10` | `129250.00` | `None` | `None` |
| `2350000.00` | `0.055` | `ADDITIVE` | `0.10` | `129250.00` | `12925.00` | `142175.00` |
| `2350000.00` | `0.055` | `INCLUDED` | `0.10` | `129250.00` | `0.00` | `129250.00` |
| `1234567.89` | `0.055` | `ADDITIVE` | `0.10` | `67901.23` | `6790.12` | `74691.35` |
| `10000000.00` | `0.055` | `ADDITIVE` | `0.10` | `550000.00` | `55000.00` | `605000.00` |
| `50000000.00` | `0.055` | `ADDITIVE` | `0.10` | `2750000.00` | `275000.00` | `3025000.00` |
| `1.00` | `0.055` | `ADDITIVE` | `0.10` | `0.06` | `0.01` | `0.07` |

The rounding case on the last row (`1 × 0.055 = 0.055`, rounds to `0.06` with ROUND_HALF_UP) must be tested — this is where `float` would give a wrong answer.

---

### Task 2.4 — Write `format_tax_result(result, language) -> str`

**File:** `tassi/tax.py` (same file, new function)

```python
def format_tax_result(result: TaxResult, language: str) -> str:
    """
    Format a TaxResult as a WhatsApp-ready message string.
    language: "fr" or "en"
    Handles UNCONFIRMED mode by showing base_acompte as confirmed
    and CAC as a clearly labelled unconfirmed estimate.
    """
```

This is the function that implements FR-TAX-2 (the transparency format) including the G1 gate language.

**Must produce different output for `UNCONFIRMED` vs `ADDITIVE`/`INCLUDED`.**

In `UNCONFIRMED` mode (current default), the French output must include language equivalent to:
> "Acompte RSI: 129 250 XAF ✓  
> CAC (non confirmé, estimation): ~12 925 XAF ⚠️  
> Consultez votre comptable pour le montant CAC exact."

---

### Task 2.5 — Write exhaustive tests

**File:** `tests/test_tax.py` (new file)

This is the most important test file in the project. Every meaningful input combination must be tested.

Test classes to write:
- `TestParseRevenue` — one test per row in the table from Task 2.1, plus extras
- `TestIsZeroReturn` — all positive and negative cases
- `TestCalculateRsi` — every row in the table from Task 2.3, plus boundary values
- `TestRoundingPrecision` — cases that would give wrong answers with `float`
- `TestFormatTaxResult` — both languages, all three cac_modes

**Done when:** `make test` passes. `grep -r "float" tassi/tax.py` returns nothing. 100% branch coverage on `tax.py`.

---

**Milestone 2 commit:**
```
feat(tax): add RSI calculation engine with exhaustive rounding tests
```

---

## Milestone 3 — Webhook Ingestion

**Goal:** Tassi can receive a WhatsApp message, acknowledge it in <500ms, and not process duplicates.
**Branch:** `feat/webhook`
**Commit prefix:** `feat(webhook):`

This milestone has no conversation logic yet. A message comes in, gets acknowledged, gets logged. The conversation state machine is Milestone 4.

---

### Task 3.1 — Meta webhook verification endpoint

**File:** `tassi/main.py` (edit existing)

```python
@app.get("/webhook", tags=["webhook"])
async def verify_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge"),
    cfg: Settings = Depends(get_settings),
) -> Response:
    """Meta's webhook verification handshake (FR-CHAT-1)."""
```

Returns `hub_challenge` as plain text if `hub_mode == "subscribe"` and token matches. Returns `403` otherwise.

**Tests:** `tests/test_webhook.py`
- `test_verify_webhook_valid` — correct token → 200 with challenge text
- `test_verify_webhook_wrong_token` → 403
- `test_verify_webhook_wrong_mode` → 403

---

### Task 3.2 — Meta webhook signature verification

**File:** `tassi/security.py` (new file)

```python
def verify_meta_signature(payload: bytes, signature_header: str, app_secret: str) -> bool:
    """
    Verify the X-Hub-Signature-256 header on incoming Meta webhooks.
    Returns True if valid, False otherwise. Never raises.
    NFR-SEC-3.
    """
```

**Implementation:** `hmac.compare_digest(computed, received)` — never use `==` for secret comparison (timing attack).

Do not put this in `main.py`. Security functions live in their own module so they can be tested in isolation and imported without importing the full app.

**Tests:** `tests/test_security.py`
- `test_valid_signature_returns_true`
- `test_wrong_signature_returns_false`
- `test_tampered_payload_returns_false`
- `test_missing_prefix_returns_false` — header must start with `"sha256="`

---

### Task 3.3 — Webhook POST endpoint

**File:** `tassi/main.py` (edit existing) + `tassi/chat.py` (new file)

```python
@app.post("/webhook", tags=["webhook"], status_code=200)
async def receive_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    cfg: Settings = Depends(get_settings),
) -> dict[str, str]:
    """
    Ingest a WhatsApp message. Acks immediately (NFR-PERF-1), 
    processes asynchronously via BackgroundTasks.
    """
    # 1. Read raw body (needed for HMAC verification)
    body = await request.body()
    
    # 2. Verify Meta signature — reject if invalid (NFR-SEC-3)
    signature = request.headers.get("X-Hub-Signature-256", "")
    if not verify_meta_signature(body, signature, cfg.meta_app_secret):
        raise HTTPException(status_code=403, detail="invalid signature")
    
    # 3. Parse the webhook payload
    # 4. Check idempotency (Redis SETNX on message_id)
    # 5. If duplicate: return {"status": "ok"} immediately
    # 6. If new: background_tasks.add_task(handle_message, message, cfg)
    # 7. Return {"status": "ok"} immediately — never make the caller wait
```

**Python rule:** Never use `await` for Campay or Meta API calls inside this route handler. All outbound calls go inside `handle_message` which runs in `BackgroundTasks`. The route handler must return within 500ms (NFR-PERF-1) regardless of what downstream services do.

**Tests:**
- `test_post_webhook_invalid_signature` → 403
- `test_post_webhook_valid_acks_immediately` → 200 `{"status": "ok"}`
- `test_post_webhook_duplicate_message_id_ignored` — same `message_id` sent twice, `handle_message` called exactly once

---

### Task 3.4 — Redis session management

**File:** `tassi/session.py` (new file)

```python
# Session state lives in Redis with TTL=2h (SDD §4)
# Key: session:<msisdn>
# Value: JSON-encoded dict of conversation state

async def get_session(redis: Redis, msisdn: str) -> dict:
    """Get current session state. Returns empty dict if no session."""

async def set_session(redis: Redis, msisdn: str, state: dict) -> None:
    """Write session state with 2h TTL."""

async def clear_session(redis: Redis, msisdn: str) -> None:
    """Delete session (on conversation end or error recovery)."""

async def is_duplicate_message(redis: Redis, message_id: str) -> bool:
    """
    SETNX on seen_msg:<message_id> with 24h TTL.
    Returns True if this message_id has been seen before.
    """

async def is_rate_limited(redis: Redis, msisdn: str) -> bool:
    """
    Increment rate_limit:<msisdn> counter with 60s TTL.
    Returns True if count exceeds threshold (FR-DATA-3).
    """
```

All functions take an explicit `redis: Redis` parameter — they do not import a global Redis client. This makes them testable with a fake/mock Redis.

**Tests:** `tests/test_session.py`
- Test all five functions with a real Redis client (use `redis://localhost:6379/1` — the test DB)
- `test_session_expires_after_ttl` — set TTL to 1 second, verify key gone after 2 seconds
- `test_is_duplicate_first_call_returns_false` — first time a message_id is seen
- `test_is_duplicate_second_call_returns_true` — same message_id seen again
- `test_rate_limit_not_exceeded` — first N calls return False
- `test_rate_limit_exceeded` — call N+1 times, returns True

**Degraded mode (NFR-AVAIL-3):** If Redis is unavailable, `get_session` returns `{}`, `set_session` and `clear_session` are no-ops, `is_duplicate_message` returns `False` (we process duplicates — acceptable under failure), `is_rate_limited` returns `False`. Wrap Redis calls in `try/except redis.RedisError` and log the failure. Never let a Redis error crash the request.

---

### Task 3.5 — Redis dependency in FastAPI

**File:** `tassi/deps.py` (new file)

```python
# FastAPI dependencies for Redis and DB session injection.
# Keeps main.py and route handlers clean.

async def get_redis(cfg: Settings = Depends(get_settings)) -> AsyncGenerator[Redis, None]:
    """Yield a Redis connection from the connection pool."""

async def get_db(cfg: Settings = Depends(get_settings)) -> AsyncGenerator[AsyncSession, None]:
    """Yield an async database session."""
```

**Done when:** `make test` passes. The test for the duplicate message scenario (Task 3.3) uses a real Redis connection.

---

**Milestone 3 commit:**
```
feat(webhook): add Meta webhook ingestion, signature verification, Redis session management
```

---

## Milestone 4 — Conversation Flow

**Goal:** A user can send a WhatsApp message and receive a correct tax calculation in reply. Both languages. Full onboarding. RESEND command. Persona T1–T6 all pass.
**Branch:** `feat/conversation`
**Commit prefix:** `feat(chat):`

This is the largest milestone. Break it into sub-tasks and commit each one.

---

### Task 4.1 — Message response templates

**File:** `tassi/templates.py` (new file)

All bot text lives in one place. No string literals scattered across other modules.

```python
# Structure: MESSAGES[language][key] = text
MESSAGES: dict[str, dict[str, str]] = {
    "fr": {
        "welcome": "...",
        "ask_language": "...",
        "ask_revenue_band": "...",
        "out_of_band": "...",
        "ask_revenue": "...",
        "zero_return_guidance": "...",
        "calculation_result": "...",   # uses .format() placeholders
        "invalid_input": "...",
        "resend_no_history": "...",
        "resend_result": "...",        # uses .format() placeholders
    },
    "en": { ... }  # same keys, English text
}
```

**Bilingual requirement (NFR-USE-1):** Every key in `"fr"` must exist in `"en"`. Write a test that asserts `set(MESSAGES["fr"].keys()) == set(MESSAGES["en"].keys())`.

**Done when:** All message keys exist in both languages. Test passes. No message text embedded in `chat.py`.

---

### Task 4.2 — Conversation state machine

**File:** `tassi/chat.py` (new file)

The conversation is a finite state machine. Each state has a name, and each incoming message triggers a transition.

```python
# States (stored in Redis session under key "state"):
# NEW              → User just messaged for the first time
# AWAITING_LANGUAGE → Bot sent language prompt, waiting for "1" or "2"
# AWAITING_BAND    → Bot sent band prompt, waiting for band selection
# ACTIVE           → Onboarding complete, ready for revenue input
# AWAITING_CONFIRM → (reserved for future confirmation flows)

async def handle_message(
    msisdn: str,
    message_text: str,
    message_id: str,
    db: AsyncSession,
    redis: Redis,
    cfg: Settings,
) -> None:
    """
    Main message handler. Called from BackgroundTasks in the webhook route.
    Reads session state, processes message, updates state, sends reply.
    """
```

**State transitions:**

```
NEW → AWAITING_LANGUAGE  (send welcome + language prompt)
AWAITING_LANGUAGE:
    "1" or "fr" → set language="fr", state=AWAITING_BAND
    "2" or "en" → set language="en", state=AWAITING_BAND
    anything else → resend language prompt
AWAITING_BAND:
    "1" (10-20M) / "2" (20-30M) / "3" (30-40M) / "4" (40-50M) → set band, state=ACTIVE
    anything else that parses as in-band → set band, state=ACTIVE
    out-of-band revenue → send FR-TAX-5 message, stay in AWAITING_BAND (don't loop forever — after 3 tries, send "contact us" message)
ACTIVE:
    is_zero_return(text) → send zero-return guidance (FR-TAX-3)
    parse_revenue(text) succeeds → calculate_rsi() → persist → send result
    "RESEND" / "RENVOYER" → fetch last tax_calculation for this user's current fiscal_period → resend (NFR-USE-4)
    parse_revenue(text) fails → send invalid_input message, stay in ACTIVE
```

**Python rule:** `handle_message` must be an async function. Database writes happen inside a single `async with db.begin()` block — if the send to Meta fails, the calculation is still saved. The send is fire-and-forget from the user's perspective; the data is durable.

---

### Task 4.3 — Meta API client

**File:** `tassi/meta.py` (new file)

```python
async def send_text_message(
    phone_number_id: str,
    access_token: str,
    recipient_msisdn: str,
    text: str,
) -> None:
    """
    Send a text message via WhatsApp Cloud API.
    Uses httpx AsyncClient. Raises on non-2xx response.
    NFR-PERF-2: called from BackgroundTasks, not from the ack path.
    """
```

**Python rule:** Create a new `httpx.AsyncClient` per call, or use a module-level client with `httpx.AsyncClient()` as a context manager. Never store an `AsyncClient` as a module-level global — it can't be properly closed.

**Tests:** `tests/test_meta.py`
- Mock `httpx.AsyncClient` — do not make real HTTP calls in tests
- `test_send_text_message_success` — 200 response, no exception
- `test_send_text_message_http_error` — 4xx/5xx response, exception is raised (so BackgroundTasks logs it)

---

### Task 4.4 — Connect everything: integration test

**File:** `tests/test_conversation.py` (new file)

These tests simulate the full conversation flow end-to-end, using a test database (via the CI Postgres service) and a mock Meta API client.

**Test scenarios to implement (from PERSONAS §5):**

- `test_T1_standard_calculation_french` — Aïssatou sends `"2 350 000 frs"`, receives correct Acompte in French
- `test_T2_standard_calculation_english` — same flow in English
- `test_T3_zero_return` — user sends `"rien"`, receives Néant guidance
- `test_T4_invalid_input_then_valid` — user sends `"abc"`, gets error, sends `"2350000"`, gets result
- `test_T5_duplicate_message_id` — same message_id twice, `send_text_message` called exactly once
- `test_T6_resend_command` — user requests RESEND, gets same result as previous calculation

**Done when:** All 6 tests pass. `make test` passes. Running a real WhatsApp message from a Meta test number produces a correct French response (manual test, done once before committing).

---

**Milestone 4 commit:**
```
feat(chat): add conversation state machine, tax calculation flow, bilingual responses
```

---

## Milestone 5 — Payments & Subscriptions

**Gate: G2 must close before this milestone goes live in production.**
The code can be written and tested. But real users cannot be charged until the licensing question is resolved.

**Branch:** `feat/payments`
**Commit prefix:** `feat(payments):`

---

### Task 5.1 — Campay API client

**File:** `tassi/campay.py` (new file)

```python
async def initiate_ussd_push(
    username: str,
    password: str,
    application_token: str,
    amount: int,
    msisdn: str,
    description: str,
    external_reference: str,
) -> str:
    """
    Initiate a USSD push payment via Campay API.
    Returns the Campay transaction reference.
    Raises on failure.
    FR-PAY-2.
    """

async def get_transaction_status(
    application_token: str,
    campay_reference: str,
) -> str:
    """
    Poll Campay for the status of a transaction.
    Returns "SUCCESS", "FAILED", or "PENDING".
    FR-PAY-4.
    """
```

**Tests:** `tests/test_campay.py`
- All tests use `httpx.MockTransport` or `pytest-httpx` — no real Campay calls in CI
- `test_initiate_ussd_push_success` — returns reference
- `test_initiate_ussd_push_http_error` — raises
- `test_get_transaction_status_success` — returns "SUCCESS"
- `test_get_transaction_status_pending` — returns "PENDING"

---

### Task 5.2 — SUBSCRIBE command handler

**File:** `tassi/chat.py` (edit existing)

Add `SUBSCRIBE` / `ABONNEMENT` to the ACTIVE state handler:

```
ACTIVE + "SUBSCRIBE" or "ABONNEMENT":
    → If already Plus: send "you are already subscribed" message
    → If not Plus: send operator selection (MTN / Orange buttons) → state=AWAITING_OPERATOR
AWAITING_OPERATOR:
    "1" MTN → initiate Campay push for MTN → create PENDING PaymentTransaction → send confirmation message → state=ACTIVE
    "2" Orange → same for Orange
```

The bot response to a SUBSCRIBE must include:
- The price (XAF 500 or whatever `PLUS_PRICE_XAF` is set to)
- Clear statement of what they get (reminders + 12 months history)
- MTN MoMo / Orange Money selection

---

### Task 5.3 — Campay webhook callback

**File:** `tassi/main.py` (edit existing) + `tassi/payments.py` (new file)

```python
@app.post("/campay/webhook", tags=["payments"], status_code=200)
async def campay_callback(
    request: Request,
    background_tasks: BackgroundTasks,
    cfg: Settings = Depends(get_settings),
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """
    Receive Campay payment status callback.
    Must verify Campay's signature/secret before processing.
    FR-PAY-3.
    """
```

**Critical security requirement (from APP.md §3.3 gap #3):** The Campay callback must be authenticated. Research Campay's callback authentication mechanism (API key header, HMAC signature, or IP allowlist) and implement it. If Campay uses a secret header, add `CAMPAY_WEBHOOK_SECRET` to `config.py` and `.env.example`. Reject unauthenticated callbacks with `403`.

In `payments.py`:
```python
async def process_payment_callback(
    campay_reference: str,
    status: str,
    db: AsyncSession,
    cfg: Settings,
) -> None:
    """
    On SUCCESS: find PENDING PaymentTransaction by campay_reference,
    update to SUCCESS, create Subscription row, send WhatsApp confirmation.
    On FAILED: update to FAILED, send WhatsApp failure message.
    Must be idempotent: if called twice with same reference, second call is a no-op.
    """
```

The idempotency is critical: Campay may send the same callback more than once. Use the `campay_reference` as a unique key and check `status` before processing. If the transaction is already `SUCCESS`, do nothing.

---

### Task 5.4 — STATUS command handler

**File:** `tassi/chat.py` (edit existing)

```
ACTIVE + "STATUS" or "STATUT":
    → Find most recent PENDING PaymentTransaction for this user
    → If none: "no pending payment found"
    → If found and >2 minutes old: poll Campay via get_transaction_status()
        → SUCCESS: same as callback (activate subscription)
        → FAILED: update record, send failure message
        → PENDING: "your payment is still processing, try again in a few minutes"
    → If found and <2 minutes old: "your payment was just initiated, wait a moment"
```

---

### Task 5.5 — HISTORY command handler

**File:** `tassi/chat.py` (edit existing)

```
ACTIVE + "HISTORY" or "HISTORIQUE":
    → If not Plus (user.is_plus == False): send "subscribe to access history"
    → If Plus: fetch last 12 tax_calculations for this user (by created_at DESC)
        → Format as a list: "Oct 2025: 129 250 XAF | Nov 2025: 141 800 XAF | ..."
        → Send as WhatsApp text (may need to split if >1 WhatsApp message limit)
```

FR-SUB-3: history is limited to 12 months.

---

### Task 5.6 — Payment integration tests

**File:** `tests/test_payments.py` (new file)

**Test scenarios (PERSONAS §5):**
- `test_T7_subscribe_mtn_success` — user sends SUBSCRIBE, selects MTN, Campay succeeds, user becomes Plus
- `test_T8_status_recovery_after_dropped_webhook` — PENDING transaction >2 min, STATUS command, Campay returns SUCCESS, subscription activated
- `test_T9_campay_callback_idempotent` — same SUCCESS callback sent twice, subscription created once
- `test_T10_failed_payment_flow` — Campay returns FAILED, user notified, remains free tier

**Done when:** All 4 tests pass. Unauthenticated Campay callback returns 403.

---

**Milestone 5 commit:**
```
feat(payments): add Campay integration, subscription management, HISTORY and STATUS commands
```

---

## Milestone 6 — Notifications & Reminders

**Goal:** Automated filing reminders and renewal prompts. Day-10 feature stays off until G3 closes.
**Branch:** `feat/reminders`
**Commit prefix:** `feat(reminders):`

---

### Task 6.1 — APScheduler setup

**File:** `tassi/reminders.py` (new file) + `tassi/main.py` (edit existing)

Wire APScheduler into the FastAPI lifespan:

```python
# In main.py lifespan:
scheduler = AsyncIOScheduler()
scheduler.add_job(daily_reminder_job, "cron", hour=3, minute=0)
scheduler.start()
yield
scheduler.shutdown()
```

The scheduler job must run in the same event loop as FastAPI. Use `AsyncIOScheduler`, not `BackgroundScheduler`.

---

### Task 6.2 — Day-14 reminder (FR-NOTIF-1)

**File:** `tassi/reminders.py`

```python
async def send_day_14_reminders(fiscal_period: str, db: AsyncSession, cfg: Settings) -> int:
    """
    Query all users who have at least one tax_calculation in fiscal_period
    AND have not already been sent a Day-14 reminder for this period.
    Send the reminder via Meta API. Return count of messages sent.
    FR-NOTIF-1.
    """
```

**Idempotency:** Track sends in a `reminders_sent` table (or a flag on `tax_calculations`). If this function is called twice on the same fiscal_period, it sends exactly zero messages the second time.

Add `reminders_sent` to `models.py` if you choose the dedicated table approach, and create a new Alembic migration for it.

---

### Task 6.3 — Day-10 reminder (FR-NOTIF-2)

**File:** `tassi/reminders.py`

```python
async def send_day_10_reminders(fiscal_period: str, db: AsyncSession, cfg: Settings) -> int:
    """
    Query all active Plus subscribers who have NOT yet filed for fiscal_period.
    Send early reminder. Feature-flagged: returns 0 immediately if
    cfg.feature_plus_reminders is False.
    FR-NOTIF-2.
    """
```

**Gate G3 dependency:** This function exists in the code but does nothing until `FEATURE_PLUS_REMINDERS=true`. Enabling it requires only an environment variable change — no code change, no deployment.

---

### Task 6.4 — Renewal prompt (FR-PAY-5)

**File:** `tassi/reminders.py`

```python
async def send_renewal_prompts(db: AsyncSession, cfg: Settings) -> int:
    """
    Query all subscriptions with period_end between now() and now()+3 days
    and status=ACTIVE. Send renewal prompt. Idempotent per subscription.
    FR-PAY-5.
    """
```

---

### Task 6.5 — Daily job wrapper

**File:** `tassi/reminders.py`

```python
async def daily_reminder_job() -> None:
    """
    Runs at 03:00 every day. Determines fiscal_period from today's date.
    Calls the appropriate reminder functions based on day of month.
    Wraps everything in try/except — a reminder failure must never crash the scheduler.
    FR-NOTIF-3.
    """
```

Error handling: if any reminder job fails, log the exception and send a WhatsApp message to the operator's own number (a hard-coded `OPERATOR_MSISDN` config variable). Never silently fail.

Add `OPERATOR_MSISDN` to `config.py` and `.env.example`.

---

### Task 6.6 — Reminder tests

**File:** `tests/test_reminders.py` (new file)

- `test_T11_day_14_reminder_sent_to_filers` — users with calculations in period receive message
- `test_T12_day_10_reminder_not_sent_when_flag_off` — `FEATURE_PLUS_REMINDERS=false`, no sends
- `test_T13_renewal_prompt_sent_3_days_before_expiry`
- `test_day_14_reminder_idempotent` — called twice, sends once
- `test_daily_job_does_not_crash_on_error` — meta API raises, job catches and logs

**Done when:** `make test` passes. Manual test: set system time to 03:00 on the 14th of a month (using `freezegun`) and verify the job fires.

---

**Milestone 6 commit:**
```
feat(reminders): add APScheduler daily reminders, renewal prompts, operator error alerting
```

---

## Milestone 7 — Production Deployment

**Goal:** Tassi is running on a real VPS, reachable by Meta's webhook, backed up nightly, monitored.
**Branch:** `chore/production`

This milestone has no Python code. It is infrastructure work. Proceed only after Milestones 1–6 are all green in CI.

---

### Task 7.1 — VPS provisioning

- [ ] Provision Hetzner CX21 (2 vCPU, 4GB RAM, €5/month) in EU region
- [ ] Create non-root deploy user with SSH key
- [ ] Install Docker + Docker Compose
- [ ] Point a domain name at the VPS IP (required for HTTPS, required for Meta webhook registration)
- [ ] Obtain TLS certificate (Caddy or Certbot) — Meta will not deliver webhooks to HTTP

---

### Task 7.2 — Production docker-compose

**File:** `docker-compose.prod.yml` (new file, **not gitignored** — no secrets in it)

```yaml
# Services: app, postgres, redis
# Volumes: postgres_data (persistent), redis_data (persistent)
# All secrets via environment variables, not in this file
# Restart policies: always
# Health checks on postgres and redis
```

---

### Task 7.3 — Environment configuration

On the VPS, create `/opt/tassi/.env` with real production values. This file lives only on the VPS — never in git, never in CI.

Verify every variable in `.env.example` has a real value in the production `.env`.

---

### Task 7.4 — Nightly backup

- [ ] Write `/opt/tassi/backup.sh` — `pg_dump` to compressed file, upload to Backblaze B2 (free tier: 10GB) or Hetzner Object Storage
- [ ] Schedule via crontab: `0 2 * * * /opt/tassi/backup.sh >> /var/log/tassi-backup.log 2>&1`
- [ ] **Do a restore drill**: download the backup file, run `pg_restore` into a clean container, verify the data is there. This must happen before go-live.

---

### Task 7.5 — Monitoring

- [ ] UptimeRobot (free tier): add a monitor on `https://your-domain.com/health`, 5-minute interval, alert to phone number
- [ ] Verify the uptime monitor sends an alert when the app is stopped (stop Docker, wait 10 minutes, confirm alert received)

---

### Task 7.6 — Meta webhook registration

- [ ] In Meta Developer Console: configure webhook URL `https://your-domain.com/webhook`
- [ ] Set `META_VERIFY_TOKEN` in production `.env` to match what Meta will send
- [ ] Subscribe to `messages` and `message_deliveries` webhook fields
- [ ] Send a test message from a real WhatsApp number, verify it arrives and gets a response

---

### Task 7.7 — Campay production credentials

- [ ] Activate Campay production account (separate from sandbox)
- [ ] Set `CAMPAY_USERNAME`, `CAMPAY_PASSWORD`, `CAMPAY_APPLICATION_TOKEN` in production `.env`
- [ ] Configure Campay webhook callback URL to `https://your-domain.com/campay/webhook`
- [ ] Run one real end-to-end payment test (actual MTN MoMo, real XAF amount) before opening to users

---

**Milestone 7 commit:**
```
chore(production): add production docker-compose and deployment documentation
```

---

## Milestone 8 — Acceptance Testing

**Goal:** All 17 PERSONAS test scenarios pass in the production (or staging) environment.

Run every scenario from PERSONAS v2.0 §5 manually with a real WhatsApp number and real (test) payments.

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
| T16 | Rounding correctness (cross-check manual calc) | `[ ]` |
| T17 | Config-driven rate change without deployment | `[ ]` |

**Done when:** All 17 rows show Pass. Any failure triggers a bug fix, re-commit, and re-test of that scenario before sign-off.

---

## Milestone 9 — Wizard-of-Oz Pilot (G3)

**Goal:** Validate that real RSI SME users will pay for Tassi Plus, and at what price.

This is not a code task. It is a business task.

- [ ] Recruit 20–30 RSI SME business owners (market associations, accountant referrals, WhatsApp groups)
- [ ] Run them through one complete filing cycle (1st → 15th of the month) on the production system
- [ ] At the end: ask directly — "would you pay for early reminders and 12 months of history? How much?"
- [ ] Collect answers. If ≥10% say yes and agree on a price → Gate G3 closes
- [ ] Update `PLUS_PRICE_XAF` in production `.env` to the validated price
- [ ] Set `FEATURE_PLUS_REMINDERS=true` in production `.env`
- [ ] Restart the app — no code change needed

**Done when:** G3 is marked closed in `docs/SRS.md` §3 with the date and validated price.

---

## Scope Enforcement — Hard Stops

If any of the following is proposed during the build phase, stop and question it:

| Proposal | Why it's out of scope |
|---|---|
| Admin dashboard or web UI | SRS §8: deferred until "DB queries become impractical" |
| PostGIS or location-based CAC | SRS §8: no validated evidence of commune-level CAC variance |
| Régime Libératoire or Réel | SRS §8: explicitly deferred |
| Celery / Redis queue | SRS §8: APScheduler sufficient for 1 daily job |
| Auto-renewing subscriptions | MoMo requires manual approval; no recurring API available |
| OCR / receipt parsing | SRS §1.2: explicitly out of scope |
| Multi-region deployment | SRS §8: single VPS until scale demands otherwise |
| ML / AI features | Not in SRS, SDD, or PERSONAS |
| Closings G1/G2/G3 in code | Gates close via real-world validation, not code changes |
