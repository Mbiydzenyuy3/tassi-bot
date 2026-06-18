# Tassi — Product Intelligence, Security & MVP Roadmap

**Version:** 1.0
**Based on:** SRS v2.0 · SDD v2.0 · PERSONAS v2.0
**Status:** Governing reference for the build phase

---

## 1. Tassi as a Data Aggregator — The Honest Picture

This is the most important section to read before writing a single line of application code, because the data Tassi collects is more sensitive — and more commercially valuable — than the product's surface appearance suggests.

### 1.1 What Tassi Actually Collects

Every user interaction writes one or more of the following to Postgres:

| Data point | Where | Sensitivity |
|---|---|---|
| MSISDN (WhatsApp phone number) | `users.whatsapp_id` | High — uniquely identifies a real person |
| Annual revenue band (10M–50M XAF) | `users.annual_revenue_band` | High — financial classification |
| Monthly gross revenue (exact figure) | `tax_calculations.gross_revenue` | Very high — actual business income |
| Filing behavior (date, frequency) | `tax_calculations.created_at` | Medium — compliance pattern |
| Payment behavior | `payment_transactions` | High — financial transaction record |
| Language preference | `users.language` | Low |
| Whether revenue was zero this month | `tax_calculations.is_zero_return` | Medium — signals business stress |

Over 12 months of use, Tassi builds a **longitudinal financial profile of every business that touches it** — monthly revenue, seasonal patterns, slow months, growth trajectory. This is data that even most banks don't have on Cameroonian SMEs.

### 1.2 Who Would Find This Data Valuable — and Why That Matters

**Group 1: Microfinance institutions and banks**
A business with 12 months of stable monthly revenue entries in Tassi's database is a far better lending risk than one with no financial history at all. Banks in Cameroon currently can't assess most informal SMEs because there is no verifiable income data. Tassi's dataset could become the basis for a micro-loan underwriting model. This is valuable to them — which means it's sensitive to your users.

**Group 2: Insurance companies**
Income protection, health, and business-continuity insurance pricing for SMEs requires income data. Tassi's append-only calculation history is exactly that.

**Group 3: Development finance institutions (World Bank, IFC, AFD)**
Aggregate, anonymised data on SME tax compliance rates, revenue trends, and formalization behavior in Cameroon is directly useful for policy research and programme design. These institutions fund research on exactly this type of informal-to-formal SME transition.

**Group 4: INS Cameroun (Institut National de la Statistique)**
The official statistics bureau has a mandate to measure the informal and semi-formal economy. Tassi's aggregate revenue data by sector, region, and filing behavior would be of genuine interest.

**Group 5: The operator (you)**
Your own dataset tells you: which revenue brackets dominate, which months are worst for SMEs, what the average Acompte amount is, how many people use the zero-return path. This is product intelligence and it also makes Tassi a credible partner for any of the groups above.

**Group 6: DGI — the one group Tassi must never serve directly**
The Direction Générale des Impôts would find this data extremely useful for identifying under-declared businesses. This is precisely why NFR-SEC-1 ("no programmatic link to DGI systems") and NFR-SEC-4 (explicit user disclosure that data is not shared with DGI) exist. This is not optional language. If users believed their data could reach DGI, the product would not exist — no RSI business owner would willingly hand their revenue figures to a service that might report them.

### 1.3 What This Means for How You Build

1. **Data minimisation is a product requirement, not just a legal nicety.** Only collect what the SRS requires. Don't add fields "for later" that aren't in the schema.
2. **NFR-SEC-4 is the most important user-facing text you will write.** The onboarding message that says "this data is not shared with DGI" must be present, clear, and in the user's language. Don't bury it.
3. **Any future data-sharing arrangement** (even anonymised, aggregate data with a bank or research institution) requires explicit user consent that goes beyond the current onboarding disclosure. This is a post-MVP decision. Don't architect for it now; just don't foreclose it either.
4. **Cameroonian data protection law applies.** Loi n°2010/012 du 21 décembre 2010 relative à la cybersécurité au Cameroun covers personal data. You are collecting MSISDN + financial figures. You need to understand your legal obligations before going live with real users.

---

## 2. Realistic User Estimates

Honest numbers only.

### 2.1 The Addressable Market

| Layer | Estimate | Source / Reasoning |
|---|---|---|
| Registered SMEs in Cameroon | ~350,000 | INS Cameroun business registry estimates |
| In RSI bracket (10M–50M XAF/year) | ~15–25% → **52,000–87,500** | RSI is the mid-tier; most small businesses are either below (Libératoire) or above this band |
| Urban, WhatsApp-active | ~70–80% of RSI bracket → **36,000–70,000** | Urban concentration of formal SMEs; WhatsApp penetration is high in Cameroonian cities |
| Plausible first-year trial users (5% of WhatsApp-active RSI SMEs) | **1,800–3,500** | 5% is a realistic free-tool adoption rate for a new, unmarketed product in an unfamiliar channel |
| Monthly active users (40–60% of trial users) | **720–2,100** | Users who send at least one revenue figure per month |

**Realistic first-year monthly active users: 500–2,000.** If you are planning infrastructure or pricing around more than this without completed G3 validation, you are making the same mistake v1.0 made.

### 2.2 Tassi Plus Conversion

If 5% of free monthly active users pay for Plus (a healthy SaaS free-to-paid conversion rate for an unproven product):

| Scenario | Free MAU | Plus subscribers | Monthly revenue (XAF 500) |
|---|---|---|---|
| Conservative | 500 | 25 | XAF 12,500 (~€10) |
| Mid | 1,000 | 50 | XAF 25,000 (~€21) |
| Optimistic | 2,000 | 100 | XAF 50,000 (~€42) |

**Brutal truth: Tassi Plus at these numbers is not a business. It is a pilot.** The pilot is what validates whether the model works at all, and what price users will actually pay. This is exactly what Gate G3 exists to discover. Hetzner CX21 costs ~€5/month. The infrastructure is cheap enough that even 25 paying users covers it. But the goal at MVP is not profitability — it is proof that people will pay for this at all.

### 2.3 What Would Change These Numbers

- **Active marketing** (WhatsApp broadcast campaigns, partnerships with accountancy firms, chambers of commerce, local market associations) could push trial-user adoption to 10–20% of the addressable base — but this requires G2 (legal clarity) to be resolved first, since aggressive marketing of a fiscal tool before you understand your licensing obligations is a real risk.
- **G1 resolving** (showing users a confident single total instead of two separate uncertain figures) would increase the tool's perceived usefulness and likely improve retention.
- **G3 resolving** at a price higher than XAF 500 would significantly improve unit economics. If the right price is XAF 1,500–2,000/month, the numbers above multiply by 3–4.

---

## 3. Security Posture

### 3.1 What Is In Place (From Day One)

| Control | How | SRS Reference |
|---|---|---|
| No DGI integration | Policy + code (no DGI API client exists) | NFR-SEC-1 |
| User disclosure: data not shared with DGI | Onboarding message (FR-CHAT-1 flow) | NFR-SEC-4 |
| Meta webhook signature verification | HMAC-SHA256 check on every inbound webhook before processing | NFR-SEC-3 |
| No float for financial data | Python `Decimal` throughout tax engine | SRS §2.5 |
| Append-only data model | No UPDATE/DELETE on `tax_calculations` or `payment_transactions` | FR-DATA-1 |
| Nightly backup | `pg_dump` to object storage, 30-day retention | FR-DATA-2 |
| Rate limiting | Per-MSISDN Redis counter, 60s TTL | FR-DATA-3 |
| Non-root Docker runtime | Dockerfile uses a `tassi` system user | SDD §10 |
| Redis-down degraded mode | Calculation works without Redis; only session state and rate limiting degrade | NFR-AVAIL-3 |
| Secret management | All credentials via environment variables; `.env` gitignored; `.env.example` has only `your-*` placeholders | Current setup |
| Pre-commit: detect-private-key | Blocks committing PEM-format key material | `.pre-commit-config.yaml` |

### 3.2 What Is Deferred (With Reason)

| Control | Why Deferred | When to Add |
|---|---|---|
| Column-level encryption (`pgcrypto`) for `gross_revenue` | Disk-level encryption on Hetzner is sufficient for one VPS with one operator | When the VPS has multiple admins or a managed DB is introduced |
| KMS / envelope encryption | Operational overhead exceeds the threat model at this scale | When user volume justifies it |
| Formal GDPR/data protection compliance audit | Cameroon's data law applies but enforcement capacity is limited; audit when volumes grow or a B2B data play is contemplated | Pre-scale |
| Penetration test | External pentest costs money; not warranted at pilot scale | Before any public launch to >500 users |

### 3.3 Gaps That Must Be Closed Before Going Live

These are not deferred — they are gaps that need to be addressed **before the first real user**:

1. **Backup verification:** The nightly `pg_dump` must be tested. A backup you've never restored is not a backup. A restore drill before go-live is mandatory.
2. **Who can access the production database directly?** The SRS assumes a single operator. If anyone else can SSH into the VPS, that's a data access control problem. Document who has access.
3. **The Campay webhook endpoint must be authenticated.** Campay should send a secret or signature with payment callbacks. Without verification, any caller could fake a `SUCCESS` webhook and activate a subscription for free. This is a critical security requirement not yet captured in the SRS — it must be implemented in `payments.py`.
4. **Rate limiting applies to the chat path — does it apply to the Campay webhook path too?** An attacker who knows your Campay callback URL could flood it. The webhook endpoint needs its own protection.
5. **Cameroonian data protection law.** Before collecting MSISDN + revenue data from real people, you need a basic legal assessment. This is not optional even at pilot scale.

---

## 4. Architecture Solidity

### 4.1 What Makes This Architecture Solid

The architecture is solid **for its stated scope**. The key design decisions that hold up to scrutiny:

**Single Postgres node is correct.** At sub-1,000 users, the complexity cost of any distributed database would vastly exceed any benefit. Postgres with `DECIMAL` types, `UUID` primary keys, append-only tables, and proper indexing on `(user_id, fiscal_period)` is genuinely the right tool. The CAP theorem discussion in SDD §3 isn't academic — it's a practical argument that adding distribution would introduce consistency trade-offs where none currently exist.

**Redis for session/idempotency is correct.** Session state is ephemeral by nature — it should be in a TTL-based store, not Postgres. The idempotency pattern (Redis `SETNX` on `message_id`) directly addresses the most common real failure mode in this environment (mobile network retries causing double processing).

**APScheduler in-process is correct.** One daily job at 03:00 querying a Postgres table with a few hundred rows does not need a message broker. Adding Celery here would add infrastructure, failure modes, and operational complexity for zero performance gain. The SRS is right to defer this.

**Stateless app layer is correct.** All state is in Postgres (durable) or Redis (ephemeral). This means horizontal scaling is a config change, not a redesign.

**Config-driven tax rates are correct.** When G1 closes and `CAC_MODE` needs to change, it's one environment variable update and a restart — no deployment, no migration, no code review.

### 4.2 Honest Weaknesses

**Single VPS is a single point of failure.** The SRS acknowledges this with NFR-AVAIL-1 ("recoverable within 1 hour"). This is acceptable for a pilot but means there will be downtime. If the VPS goes down on the 13th of the month, users who haven't filed yet will miss the reminder window. This is a known, accepted trade-off — not a design flaw — but it needs to be communicated honestly.

**No monitoring beyond a health check.** If the daily cron job fails silently, no one will know until users complain about missing reminders. Before going live, you need at minimum: a cron job that emails/messages you if it fails, and an uptime monitor (UptimeRobot, free tier, sufficient) on `/health`.

**The `is_plus` boolean on `users` is derived state.** Its true value is whether a `subscriptions` row exists with `status='ACTIVE'` and `period_end > now()`. If these get out of sync (e.g., the Campay webhook marks `SUCCESS` but the `users.is_plus` update fails mid-transaction), you have a data integrity problem. The payment flow must use a single database transaction that updates both, or `is_plus` must be computed dynamically from `subscriptions` rather than stored directly.

**The 14th-day reminder could send to a user twice** if the cron job is run manually for testing and then also runs on schedule. The query in `reminders.py` needs an explicit `fiscal_period` guard to prevent duplicate sends.

---

## 5. MVP Milestones

These milestones are derived strictly from SRS v2.0, SDD v2.0, and PERSONAS v2.0. Nothing in this list is speculative or out of scope. If a task isn't traceable to an FR, an NFR, or an edge case in the PERSONAS, it doesn't belong here.

Each milestone has a **Definition of Done** — a test passes or a real behavior is observable. "I think it works" is not done.

---

### Pre-Build: Close the Validation Gates (Before Milestone 1 Begins)

This is the section most likely to be skipped. It should not be.

| Gate | Action Required | Why It Can't Wait |
|---|---|---|
| **G1 — Tax formula** | Consult a licensed Cameroonian tax professional. One meeting. One written answer: is CAC additive or included in the 5.5% RSI rate? | You are building a tax calculator. If the formula is wrong, the core product is wrong. The SRS handles G1 being open with the "unconfirmed" transparency format — but shipping to real users with known formula uncertainty is a reputational risk. Resolve this before Milestone 4 goes live. |
| **G2 — Legal** | Consult a Cameroonian business/consumer-law professional. One meeting. One written answer: does selling Tassi Plus constitute regulated fiscal-advisory activity? | You cannot take money from users for a tax-related service without knowing whether you need a licence to do so. Payments (Milestone 5) cannot go live until G2 closes. |
| **G3 — Pricing & demand** | Run the Wizard-of-Oz pilot: use a WhatsApp group + spreadsheet to manually serve 20–30 real RSI SME users through one filing cycle. Ask them directly if they'd pay, and at what price. | Building the full subscription/payment stack before validating demand is how v1.0's monetisation mistake happened. G3 can run in parallel with Milestones 1–3 (which don't touch payments). But Milestone 5 should not begin until G3 closes. |

---

### Milestone 1 — Database Layer

**Branch:** `feat/database-layer`
**What gets built:** `tassi/db.py`, `tassi/models.py`, first Alembic migration

**Deliverables:**
- `db.py`: SQLAlchemy engine + session factory, reads `DATABASE_URL` from config
- `models.py`: four tables per SDD §5 — `users`, `tax_calculations`, `subscriptions`, `payment_transactions`
- Alembic migration: `0001_initial_schema.py` — creates all four tables with correct types, constraints, and indexes
- `tests/test_models.py`: tests that all models can be instantiated and that the `(user_id, fiscal_period)` index exists on `tax_calculations`

**FRs satisfied:** FR-DATA-1 (append-only schema), SDD §5 schema

**Definition of Done:**
- `make migration MSG="initial schema"` produces a valid migration file
- `make migrate` runs against a clean test database without error
- `make test` passes (coverage maintained at 100%)
- `is_plus` on `users` is implemented as a property computed from `subscriptions`, **not** as a stored boolean — addressing the data integrity weakness identified in §4.2 of this document

**Gate dependency:** None — schema is independent of G1, G2, G3.

---

### Milestone 2 — Tax Calculation Engine

**Branch:** `feat/tax-engine`
**What gets built:** `tassi/tax.py`

**Deliverables:**
- `calculate_rsi(gross_revenue, cac_mode, rate_rsi, cac_rate)` — pure function, no I/O, exactly as specified in SDD §6
- Input parsing: `parse_revenue(raw: str) -> Decimal | None` — strips non-digits, handles all NFR-USE-2 formats
- Zero-revenue detection: `is_zero_return(raw: str) -> bool` — recognises "0", "rien", "néant", "nothing", "0.00", etc.
- `tests/test_tax.py`: exhaustive rounding tests, every meaningful boundary value, every `cac_mode` branch — this file should be the longest test file in the project

**FRs satisfied:** FR-TAX-1, FR-TAX-2, FR-TAX-3 (pure logic only), FR-CHAT-3 (parsing), NFR-USE-2, NFR-MAINT-1

**Non-negotiable test cases (if any of these are missing, this milestone is not done):**

| Input | cac_mode | Expected base_acompte | Expected cac_amount |
|---|---|---|---|
| `Decimal("2350000.00")` | `UNCONFIRMED` | `Decimal("129250.00")` | `None` |
| `Decimal("2350000.00")` | `ADDITIVE` | `Decimal("129250.00")` | `Decimal("12925.00")` |
| `Decimal("2350000.00")` | `INCLUDED` | `Decimal("129250.00")` | `Decimal("0.00")` |
| `Decimal("1234567.89")` | `ADDITIVE` | `Decimal("67901.23")` | `Decimal("6790.12")` |
| `"2.350.000 frs"` | — | parses to `Decimal("2350000.00")` | — |
| `"1,500,000"` | — | parses to `Decimal("1500000.00")` | — |
| `"1 500 000"` | — | parses to `Decimal("1500000.00")` | — |
| `"abc"` | — | returns `None` | — |
| `"rien"` | — | `is_zero_return = True` | — |
| `"0"` | — | `is_zero_return = True` | — |

**Definition of Done:**
- `make test` passes with 100% coverage on `tax.py`
- Every table row above has a named test case
- Zero `float` usage anywhere in `tax.py` — enforced by grep in CI or a linting rule

**Gate dependency:** G1 does not block building this. The `UNCONFIRMED` mode is the valid ship state. But if G1 resolves before this milestone completes, implement the confirmed mode at the same time.

---

### Milestone 3 — Webhook Ingestion + Chat Layer

**Branch:** `feat/chat-layer`
**What gets built:** `tassi/chat.py`, webhook route in `tassi/main.py`

**Deliverables:**
- `POST /webhook` endpoint: validates Meta signature (NFR-SEC-3), acknowledges with `200 OK` within 500ms (NFR-PERF-1), then processes asynchronously via FastAPI's background task
- `GET /webhook` endpoint: Meta's webhook verification challenge (required for WhatsApp Cloud API setup)
- Redis session management: `get_session(msisdn)`, `set_session(msisdn, state)`, `clear_session(msisdn)` — all with TTL 2h
- Idempotency: `is_duplicate(message_id)` using `SETNX` — if True, ack and return immediately
- Rate limiting: `is_rate_limited(msisdn)` using Redis counter with 60s TTL
- User creation on first contact (delegates to `db.py`)
- Language detection and persistence (FR-CHAT-4)
- Degraded mode: if Redis is unavailable, session is stateless (no multi-turn) but calculation still works (NFR-AVAIL-3)

**FRs satisfied:** FR-CHAT-1, FR-CHAT-2, FR-CHAT-4, FR-CHAT-5, FR-CHAT-6, NFR-SEC-3, NFR-PERF-1, FR-DATA-3, NFR-AVAIL-3

**Definition of Done:**
- `tests/test_webhook.py` covers:
  - Valid webhook processes correctly
  - Invalid Meta signature returns 403
  - Duplicate `message_id` returns 200 but takes no action
  - Rate-limited MSISDN returns 200 but takes no action
  - Redis-down scenario: calculation proceeds without session state
- `make test` passes at 100% coverage
- PERSONAS test scenario T5 (duplicate delivery) passes as an integration test

---

### Milestone 4 — Full Calculation Flow End-to-End

**Branch:** `feat/calculation-flow`
**What gets built:** Connects Milestones 1–3 into a complete user-visible flow

**Deliverables:**
- Onboarding conversation: language choice → revenue band question → band validation (FR-TAX-5)
- Calculation response: revenue input → parse → `calculate_rsi()` → persist to `tax_calculations` → reply in FR-TAX-2 format
- Déclaration Néant path: zero-revenue input → guidance message (FR-TAX-3)
- `RESEND` command: re-sends most recent `tax_calculations` row (NFR-USE-4)
- Bilingual responses: all bot messages in both FR and EN (NFR-USE-1)
- Onboarding rejection: out-of-band revenue responses to clear "Tassi doesn't yet cover your bracket" (FR-TAX-5)

**FRs satisfied:** FR-TAX-1, FR-TAX-2, FR-TAX-3, FR-TAX-4, FR-TAX-5, NFR-USE-1, NFR-USE-2, NFR-USE-3, NFR-USE-4

**Definition of Done:**
- PERSONAS test scenarios **T1, T2, T3, T4, T5, T6** all pass
- A real WhatsApp message to the development Meta app ID produces a correct response (manual test)
- Aïssatou Bello's complete walkthrough (PERSONAS §2) can be executed step-by-step with the expected outputs at each stage

**Gate dependency:** G1 should be resolved before this milestone is deployed to production users. You can complete and test it with G1 open (the `UNCONFIRMED` display mode works), but do not give the calculator's URL to real users until you are confident the formula is correct.

---

### Milestone 5 — Payments & Subscription

**Branch:** `feat/payments`
**What gets built:** `tassi/payments.py`

**⚠️ Hard gate: Do not start this milestone until G2 closes.** Taking money from users for a tax-related service without legal clarity is not worth the risk. The code can be written in parallel, but it cannot go live.

**Deliverables:**
- `SUBSCRIBE` / `ABONNEMENT` command: presents MTN MoMo / Orange Money buttons (FR-SUB-1, FR-PAY-1)
- Campay USSD push: creates `PENDING` payment record, calls Campay API (FR-PAY-2)
- Non-blocking response: bot replies "processing, send STATUS if no confirmation in 2 minutes" (FR-PAY-3)
- `POST /campay/webhook` endpoint: verifies Campay's callback, marks `SUCCESS`/`FAILED`, activates subscription (FR-PAY-3)
  - **This endpoint must verify the Campay signature/secret** — missing from SRS, must be added here
- `STATUS` command: polls Campay directly for `PENDING` transactions >2 minutes old (FR-PAY-4)
- `HISTORY` / `HISTORIQUE` command: returns last 12 `tax_calculations` for Plus subscribers (FR-SUB-3)
- `HISTORY` for non-Plus users: prompts to subscribe
- Plus subscriber detection via `subscriptions` query (not `users.is_plus` boolean — see §4.2)
- Subscription activation/expiry logic: `subscriptions.status`, `period_start`, `period_end`

**FRs satisfied:** FR-SUB-1, FR-SUB-2, FR-SUB-3, FR-PAY-1, FR-PAY-2, FR-PAY-3, FR-PAY-4, FR-DATA-1

**Definition of Done:**
- PERSONAS test scenarios **T7, T8, T9, T10** pass
- T8 (dropped webhook + STATUS recovery) is tested with a real Campay sandbox call, not mocked
- The Campay callback endpoint rejects requests without a valid signature (critical security test)
- Robert Mballa's complete walkthrough (PERSONAS §3) through Story 2.2 executes with expected outputs

**Gate dependency:** G2 must close before this goes live. G3 should close before the XAF 500 placeholder price is made public.

---

### Milestone 6 — Notifications & Reminders

**Branch:** `feat/reminders`
**What gets built:** `tassi/reminders.py`

**Deliverables:**
- `send_day_14_reminders(fiscal_period)`: queries all users with ≥1 `tax_calculations` row in `fiscal_period`, sends FR-NOTIF-1 message to each. Must be idempotent — running twice on the same day must not send twice. Track sends with a `reminder_sent_at` field or a `reminders_sent` table.
- `send_day_10_reminders(fiscal_period)`: queries all Plus subscribers, sends FR-NOTIF-2 message. Feature-flagged off (`FEATURE_PLUS_REMINDERS=false` until G3 closes).
- `send_renewal_prompts()`: queries subscriptions with `period_end` between `now()` and `now() + 3 days`, sends FR-PAY-5 message.
- APScheduler job at 03:00 daily wiring all three together (FR-NOTIF-3).
- Idempotency guard: if the scheduler fires twice (e.g., manual test + scheduled), no double-sends.

**FRs satisfied:** FR-NOTIF-1, FR-NOTIF-2, FR-NOTIF-3, FR-PAY-5, FR-SUB-4, FR-SUB-5

**Definition of Done:**
- PERSONAS test scenarios **T11, T12, T13** pass
- T12 (Day-10 reminder with flag off) is explicitly tested — no messages sent
- The idempotency guard is tested: running the Day-14 function twice produces exactly one reminder per user
- A manual cron test with `today.day == 14` sends to the correct users in the test database

**Gate dependency:** FR-NOTIF-2 (Day-10) stays off until G3 closes. The code exists but is guarded.

---

### Milestone 7 — Production Deployment

**Branch:** `chore/production-setup`
**This is infrastructure work, not feature work.**

**Deliverables:**
- VPS provisioned (Hetzner CX21 or equivalent, EU region)
- `docker-compose.yml` confirmed running in production with real environment variables
- Nightly `pg_dump` to S3-compatible object storage (e.g., Backblaze B2 or Hetzner Object Storage) — scheduled via cron
- **Restore drill completed** — the backup must be tested before go-live, not assumed to work
- Uptime monitor configured (UptimeRobot free tier, checking `/health` every 5 minutes, alerts to a phone number)
- Failed-cron alerting: if the daily job fails, an alert is sent (simple try/except wrapper that messages you on WhatsApp via the same Meta API)
- Meta webhook registered pointing to `https://your-domain.com/webhook`
- Campay production credentials active
- `RATE_RSI`, `CAC_MODE`, `CAC_RATE` set to confirmed values (if G1 is closed) or `UNCONFIRMED` (if not)
- `PLUS_PRICE_XAF` set to G3-validated price (if closed) or placeholder

**Definition of Done:**
- `GET https://your-domain.com/health` returns `{"status": "ok"}`
- A real WhatsApp message from a test number produces a correct calculation response
- A restore from the nightly backup has been tested on a separate machine/container
- The uptime monitor has fired at least one test alert

---

### Milestone 8 — Acceptance Testing

**Branch:** No new code — this is a testing phase on `development`

**Deliverables:**
- All 17 test scenarios from PERSONAS §5 executed manually against the production (or staging) environment
- Each scenario documented as Pass/Fail with evidence
- Any failure results in a bug fix committed and re-tested before sign-off

**Critical scenarios that cannot be skipped:**
- **T5** (duplicate webhook): must be tested against the real Meta API, not just in unit tests
- **T8** (dropped webhook + STATUS): must be tested against Campay sandbox
- **T15** (Redis-down degraded mode): Redis must actually be stopped, not mocked
- **T16** (rounding correctness): already covered by unit tests but must be cross-checked against a manual calculation
- **T17** (config-driven rate change): change `RATE_RSI` on the running VPS, restart, verify new calculation uses new rate without any code change

**Definition of Done:**
- All 17 scenarios documented as Pass
- No P0 or P1 bugs outstanding

---

### Milestone 9 — Wizard-of-Oz Pilot (G3)

**This is not a code milestone. It is a business validation milestone.**

Run the G3 pilot from SRS §3:
- Recruit 20–30 real RSI SME business owners via WhatsApp groups, market associations, or accountants
- Serve them manually for one complete filing cycle (1st → 15th of the month)
- At the end: ask directly whether they'd pay for the Plus tier and what price feels fair
- Measure: Did they use it? Did they share it? Did the Day-14 reminder actually drive action?

**What closes G3:**
- Evidence that ≥10% of pilots would pay for Tassi Plus
- A validated price point (not guessed)
- Qualitative feedback on what was confusing vs. what worked

**What happens after G3:**
- Set `PLUS_PRICE_XAF` to the validated price
- Enable `FEATURE_PLUS_REMINDERS=true`
- Update SRS §3 to mark G3 closed

---

## 6. Scope Enforcement Rules for the Build Phase

These rules apply to every PR. If a piece of work can't be traced to an FR, an NFR, or an edge case in PERSONAS v2.0, it is out of scope and will not merge.

1. **No PostGIS.** CAC is a flat config value (`CAC_RATE=0.10`). If someone proposes a `communes` table, they must first produce evidence of genuine commune-level CAC variance in the current CGI. Until then: rejected.

2. **No Régime Libératoire or Régime Réel.** Both are explicitly deferred in SRS §8. If the tax professional consulted for G1 provides validated formulas for these regimes, they go into the backlog — not into the current branch.

3. **No admin dashboard.** Direct Postgres queries (`psql` or a desktop client like DBeaver) are sufficient for an operator managing hundreds of users. This is deferred in SRS §8 until "direct DB queries become impractical."

4. **No Celery.** APScheduler in-process handles one daily job. Celery is deferred until the cron job demonstrably can't keep up.

5. **No auto-renewing subscriptions.** MoMo requires manual approval per payment. If a MoMo aggregator offering real recurring billing is identified, this goes on the backlog.

6. **No OCR or receipt parsing.** SRS §1.2 explicitly excludes this.

7. **If a Gate is still open, don't pretend it's closed.** `CAC_MODE=UNCONFIRMED` stays as the default until G1 closes in writing. `FEATURE_PLUS_REMINDERS=false` stays off until G3 closes. No one overrides this in code.
