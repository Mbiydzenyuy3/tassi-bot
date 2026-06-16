# Tassi Software Design Document (SDD)

**Version:** 2.0 (Realistic MVP)
**Based on:** Tassi SRS v2.0
**Supersedes:** v1.0 (modular monolith, PostGIS, multi-app, Celery, multi-instance)
**Architecture Style:** Single service, single database, stateless app layer
**Technology Stack:** Python (FastAPI), PostgreSQL, Redis, APScheduler/cron, Meta WhatsApp Cloud API, Campay

---

## 1. Introduction

### 1.1 Purpose

This document describes the architecture for Tassi MVP — deliberately the *smallest* design that satisfies SRS v2.0, not the largest one that could plausibly be justified. Every component included here has a concrete requirement behind it; every component from v1.0 that didn't (PostGIS, Celery, Next.js admin, multi-instance deployment) has been removed and listed in §8 as deferred, with the condition that would bring it back.

---

## 2. High-Level Architecture

```
┌─────────────────────────────┐
│   User's WhatsApp App        │
└───────────────┬───────────────┘
                 │ HTTPS (Meta-managed delivery & retries)
┌───────────────▼───────────────┐
│   Meta WhatsApp Cloud API      │
└───────────────┬───────────────┘
                 │ Webhook (HTTPS)
┌───────────────▼────────────────────────────┐
│            Single VPS (EU region)           │
│                                              │
│   ┌────────────────────────────────────┐   │
│   │   FastAPI app (single process)      │   │
│   │   - webhook handler                 │   │
│   │   - tax calculation engine          │   │
│   │   - payment/subscription logic      │   │
│   │   - daily reminder job (in-process  │   │
│   │     APScheduler, no Celery)         │   │
│   └──────────┬─────────────┬───────────┘   │
│              │             │                │
│   ┌──────────▼───┐   ┌─────▼──────┐         │
│   │  PostgreSQL   │   │   Redis    │         │
│   │  (single node)│   │ session/   │         │
│   │               │   │ idempotency│         │
│   └───────────────┘   └────────────┘         │
└───────────────┬─────────────────────────────┘
                 │ HTTPS
┌───────────────▼───────────────┐
│   Campay (MTN MoMo / Orange)   │
└─────────────────────────────────┘
```

**Why EU-region hosting, not in-country:** Cameroon-to-EU latency (~120-180ms) is negligible against the 1.2s reply budget (NFR-PERF-2), where the dominant latency is the user's mobile network delivering the WhatsApp message — not server-to-server hops. EU VPS providers (e.g., Hetzner) are cheaper and more operationally mature than regional alternatives at this scale.

---

## 3. CAP Theorem — Applied Honestly

This section exists because "use the CAP theorem" was a stated requirement, and the honest application of it here is mostly to say **where it doesn't apply**, so effort isn't wasted solving a distributed-systems problem this product doesn't have.

### 3.1 The database is not distributed — CAP doesn't constrain it

CAP theorem governs trade-offs **between nodes of a replicated data store during a network partition between those nodes**. Tassi runs **one Postgres instance**. There is no partition to have a trade-off about — a single node gives full Consistency and Availability via standard ACID transactions. Introducing a distributed database (multi-region Postgres, Cassandra, etc.) here would *create* a CAP trade-off where none currently exists, for no requirement that needs it (SRS §1.2 explicitly scopes this out).

### 3.2 The real partitions: Meta and Campay

The boundaries that are **actually, routinely partitioned** — because Cameroonian mobile networks drop connections regularly — are:

| Boundary | Partition behavior | Design choice | Requirement |
|---|---|---|---|
| Meta → Tassi webhook | Meta retries on timeout/no-ack; users also manually resend messages they think failed | **AP**: accept the message, dedupe, never let a retry cause a double reply or double calculation | FR-CHAT-6 |
| Tassi → Campay, Campay → Tassi | USSD PIN approved, but the success webhook may not arrive (classic "network droppage during PIN entry") | **AP**: respond to the user optimistically ("processing"), record `PENDING`, reconcile via polling | FR-PAY-3, FR-PAY-4 |

**The pattern in both cases is the same:** never let an external system's unavailability block a user-facing response (Availability), accept that the two sides may briefly disagree about state (give up strong Consistency across that boundary), and converge later via idempotent dedup or polling reconciliation (Partition tolerance, handled explicitly rather than ignored).

### 3.3 Summary

| Layer | CAP-relevant? | Choice | Mechanism |
|---|---|---|---|
| FastAPI ↔ Postgres/Redis (same VPS) | No — not distributed | Full C+A | Standard transactions |
| FastAPI ↔ Meta | Yes | AP | `message_id` dedup (FR-CHAT-6) |
| FastAPI ↔ Campay | Yes | AP | `PENDING` + poll reconciliation (FR-PAY-3/4) |

---

## 4. Application Structure

```
tassi/
├── main.py              # FastAPI app, webhook routes
├── config.py            # RATE_RSI, CAC_MODE, CAC_RATE, Plus price — all env-driven
├── db.py                 # SQLAlchemy engine/session
├── models.py             # users, tax_calculations, subscriptions, payment_transactions
├── chat.py               # session state (Redis), language, message parsing (FR-CHAT)
├── tax.py                 # calculation engine (FR-TAX) — Decimal only
├── payments.py            # Campay integration, subscription logic (FR-PAY, FR-SUB)
├── reminders.py           # APScheduler daily job (FR-NOTIF)
└── tests/
    ├── test_tax.py        # rounding & rate-config tests
    └── test_webhook.py    # idempotency / dedup tests
```

One service. One repo. No `apps/` package hierarchy — that structure was scaffolding for a multi-team, multi-domain system this product isn't yet.

---

## 5. Domain Model & Database Schema

```
users 1───* tax_calculations
users 1───0..1 subscriptions 1───* payment_transactions
```

**users**

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| whatsapp_id | VARCHAR(32) UNIQUE | MSISDN |
| language | ENUM('fr','en') | default 'fr' |
| annual_revenue_band | ENUM('UNDER_10M','RSI_10_50M','OVER_50M','UNKNOWN') | set at onboarding, FR-TAX-5 |
| is_plus | BOOLEAN | default false |
| created_at | TIMESTAMP | |

**tax_calculations** (append-only, FR-DATA-1)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK | |
| gross_revenue | DECIMAL(15,2) | |
| base_acompte | DECIMAL(15,2) | RATE_RSI applied |
| cac_amount | DECIMAL(15,2) | computed per `CAC_MODE`, may be NULL pre-G1 |
| cac_mode_used | VARCHAR(16) | `'ADDITIVE'` \| `'INCLUDED'` \| `'UNCONFIRMED'` — records which rule was active, for later correction if G1 changes the answer |
| fiscal_period | VARCHAR(7) | `YYYY-MM` |
| is_zero_return | BOOLEAN | FR-TAX-3 |
| created_at | TIMESTAMP | |

**subscriptions**

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK UNIQUE | one active subscription per user |
| status | ENUM('ACTIVE','EXPIRED') | |
| period_start / period_end | TIMESTAMP | manual-renewal model, FR-SUB-2 |

**payment_transactions** (append-only)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| subscription_id | UUID FK | |
| reference | VARCHAR(128) UNIQUE | Campay token |
| amount | DECIMAL(10,2) | config-driven price |
| status | ENUM('PENDING','SUCCESS','FAILED') | |
| payment_method | ENUM('MTN_MOMO','ORANGE_MONEY') | |
| created_at / settled_at | TIMESTAMP | |

**Redis (no Postgres tables needed for these — ephemeral by design)**

- `session:<msisdn>` — current conversation step, TTL 2h (FR-CHAT-2)
- `seen_msg:<message_id>` — idempotency marker, short TTL (FR-CHAT-6)
- `rate_limit:<msisdn>` — counter, TTL 60s (FR-DATA-3)

**What was removed from v1.0 and why:**
- `communes` table + PostGIS: no evidence of commune-level CAC variance (SRS §1.2); CAC is a flat config value (`CAC_RATE`).
- `session_states` as a Postgres table: session state is inherently ephemeral — Redis with a TTL *is* the correct store; persisting it to Postgres added a table with no durability requirement.

---

## 6. Tax Calculation Engine (FR-TAX)

```python
from decimal import Decimal

def calculate_rsi(gross_revenue: Decimal, cac_mode: str, rate_rsi: Decimal, cac_rate: Decimal) -> dict:
    base_acompte = (gross_revenue * rate_rsi).quantize(Decimal("0.01"))
    if cac_mode == "ADDITIVE":
        cac_amount = (base_acompte * cac_rate).quantize(Decimal("0.01"))
    elif cac_mode == "INCLUDED":
        cac_amount = Decimal("0.00")  # already inside base_acompte; shown for breakdown only
    else:  # UNCONFIRMED — default until G1 closes
        cac_amount = None
    return {"base_acompte": base_acompte, "cac_amount": cac_amount, "cac_mode": cac_mode}
```

`rate_rsi` defaults to `0.055`, `cac_rate` to `0.10`, `cac_mode` defaults to `"UNCONFIRMED"`. Every value is read from `config.py` (env vars) per NFR-MAINT-1 — changing the answer to G1 is a config change, not a code change.

---

## 7. Payment & Subscription Flow (FR-PAY, FR-SUB)

```
User sends SUBSCRIBE
        │
        ▼
Bot shows [MTN MoMo] [Orange Money]
        │
        ▼
Create payment_transactions row (PENDING) ──► Call Campay (USSD push)
        │
        ▼
Bot replies: "Processing — we'll confirm shortly. Send STATUS if you don't hear back in 2 minutes."
        │
   ┌────┴─────────────────────────┐
   ▼ (Campay webhook arrives)      ▼ (user sends STATUS, or webhook never arrives)
Mark SUCCESS, activate              Poll Campay directly (FR-PAY-4),
subscriptions row, confirm           then mark SUCCESS/FAILED accordingly
```

This is the AP pattern from §3.2 applied concretely: the bot never sits in a blocking loop waiting for Campay.

**3 days before `period_end`:** FR-PAY-5 sends a renewal prompt. There is no silent auto-debit — MoMo collection via Campay is a one-shot USSD push per attempt, so "subscription" here means "recurring manual approval," and the design doesn't pretend otherwise.

---

## 8. Reminders (FR-NOTIF)

A single daily APScheduler job inside the FastAPI process:

```
03:00 daily:
  if today.day == 14:
      for user in users who calculated this fiscal_period:
          send "filing window closes tomorrow" (FR-NOTIF-1)
  if today.day == 10 and FEATURE_PLUS_REMINDERS_ENABLED:  # off until G3
      for user in users where is_plus:
          send Day-10 reminder (FR-NOTIF-2)
```

No Celery, no message broker. At the user volumes where this MVP operates, a daily in-process job querying Postgres directly is sufficient and removes an entire piece of infrastructure (and its failure modes) from the system.

---

## 9. Security

- **NFR-SEC-3:** Meta webhook signature verified on every request before any processing.
- **NFR-SEC-2:** Postgres-level encryption at rest (managed VPS provider's disk encryption, or `pgcrypto` for the `gross_revenue`/`base_acompte` columns specifically). Full envelope encryption with a separate KMS is deferred — it's real defense-in-depth, but at one VPS with one operator, the disk-encryption baseline is the proportionate control until there's a team/infra surface that justifies more.

---

## 10. Deployment & Operations

- **Single VPS** (e.g., Hetzner CX21 or equivalent), Postgres + Redis + the FastAPI app via `systemd` or a single `docker-compose.yml`.
- **Nightly `pg_dump`** to S3-compatible object storage, 30-day retention (FR-DATA-2).
- **Code freeze, 8th–16th of each month** (NFR-AVAIL-2) — the one operational rule that matters most, given that load and "if this breaks, everyone is affected at once" both peak in that window.
- **Manual portal-mapping check**, once a month before the 1st — a calendar reminder for the operator to confirm the DGI Harmony field layout hasn't changed (feeds FR-SUB-5 for Plus subscribers).

---

## 11. Failure Modes & Mitigations

| Failure Mode | Mitigation |
|---|---|
| Meta retries a webhook (duplicate delivery) | FR-CHAT-6 idempotency via `seen_msg:<message_id>` |
| Campay webhook lost after PIN approval | FR-PAY-4 `STATUS` command + poll |
| Redis down | NFR-AVAIL-3 — calculation path (highest value) degrades gracefully, doesn't fail |
| VPS down entirely | Restore from nightly `pg_dump` (NFR-AVAIL-1) — accepted RTO ~1 hour |
| DGI Harmony portal layout changes | Manual monthly check (§10) updates config; Plus subscribers notified (FR-SUB-5) |
| G1 unresolved indefinitely | Product still works — FR-TAX-2's transparent "confirmed/unconfirmed" framing is a permanent fallback, not just a placeholder |

---

## 12. Scaling Path (deferred until triggered)

| Trigger | Response |
|---|---|
| Single VPS CPU/memory consistently saturated | Vertical resize first (cheapest, no architecture change) |
| Reporting/analytics queries slow down the main DB | Add a read replica |
| >1,000 concurrent webhook bursts | Second FastAPI instance behind a load balancer — trivial because the app is already stateless (NFR-SCALE-1) |
| Daily reminder job takes too long for one process | Move to a proper scheduler — still not Celery unless job *types* multiply, not just job *volume* |
| Genuine evidence of per-commune CAC variance | Add a two-column `communes` lookup table — still no PostGIS unless polygon-based geolocation becomes an actual requirement |

Nothing in this table is built preemptively. Each row is a condition to watch for, not a task to schedule.
