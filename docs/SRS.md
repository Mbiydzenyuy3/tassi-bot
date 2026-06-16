# Tassi Software Requirements Specification (SRS)

**Version:** 2.0 (Realistic MVP)
**Status:** Draft — governs current build scope
**Supersedes:** v1.0 (full-scale "production" draft)
**Target System:** WhatsApp Business Cloud API & a single FastAPI service

---

## 0. Document History & Relationship to v1.0

v1.0 described a multi-app, PostGIS-backed, multi-regime, Celery-driven platform sized for 20,000 users. Critical review (see project discussion log) found that:

- The tax formula it assumed had not been validated against the current Code Général des Impôts and may not apply to the segments it targeted.
- Its monetization model (a one-off "blueprint" paywall) had no recurring value once a user learned the static line-number mapping.
- Its architecture (PostGIS, admin dashboard, Celery, multi-instance deployment) was sized for a scale and complexity this product has not earned or needed.

**v2.0 replaces it as the governing spec.** It targets a single validated tax regime, a single small server, and a monetization model built around genuinely recurring value (reminders + filing history), with open questions tracked explicitly as **Validation Gates** rather than hidden inside "Approved" requirements.

---

## 1. Introduction

### 1.1 Purpose

Defines the requirements for Tassi MVP: a WhatsApp bot that computes the monthly Acompte (advance tax) for Cameroonian SMEs under **Régime Simplifié (RSI)**, with an optional paid tier ("Tassi Plus") for reminders and filing history.

### 1.2 Scope

**In scope (v2.0):**
- Free, on-demand Acompte calculation for RSI taxpayers (annual revenue 10M–50M XAF)
- Zero-revenue ("Déclaration Néant") detection and guidance
- A single optional paid tier ("Tassi Plus") providing proactive reminders and a 12-month filing history
- Mobile Money payment via Campay for Tassi Plus
- One VPS, one Postgres database, Redis for session/idempotency, a cron-based reminder job

**Explicitly out of scope (deferred — see §8):**
- Régime Libératoire and Régime Réel (different mechanics, unvalidated — see G1)
- PostGIS / commune-level CAC variance (no evidence it exists — see SDD §3)
- Admin web dashboard (direct DB access is sufficient at this scale)
- Multi-region deployment, Celery, microservice decomposition
- OCR / receipt photo parsing

### 1.3 Definitions, Acronyms & Abbreviations

| Term | Definition |
|---|---|
| DGI | Direction Générale des Impôts |
| Acompte | Monthly advance tax payment |
| CAC | Centimes Additionnels Communaux — a 10% communal surcharge on certain taxes (Art. 581 CGI) |
| RSI | Régime Simplifié d'Imposition — annual revenue 10M–50M XAF, 5.5% Acompte rate |
| Déclaration Néant | Mandatory zero/nil tax return |
| MSISDN | The user's WhatsApp phone number, used as account identifier |
| XAF | Central African CFA Franc |
| AP / CP | Availability+Partition-tolerance vs. Consistency+Partition-tolerance (CAP theorem) — see SDD §3 |

### 1.4 References

- Tassi SDD v2.0
- Code Général des Impôts du Cameroun (provisions on RSI Acompte and Art. 581 CAC)
- Meta WhatsApp Business Cloud API documentation
- Campay API documentation

---

## 2. General Description

### 2.1 Product Perspective

Tassi is a single WhatsApp bot, backed by a single small server. It does not integrate with DGI systems. It has two tiers:

- **Free:** calculate Acompte on demand, get zero-return guidance.
- **Tassi Plus (paid):** the above, plus Day-10 reminders, a 12-month filing history, and a kept-current DGI Harmony field-mapping reference.

### 2.2 Product Functions

```
Inbound WhatsApp message
        │
        ▼
 Parse & sanitize number ──► Compute Acompte (RSI, 5.5%) ──► Reply with figures
        │                                                          │
        │                                                          ▼
        │                                          (if Plus) store to filing history
        ▼
 Zero detected? ──► Déclaration Néant guidance
```

### 2.3 User Classes & Characteristics

| User Class | Characteristics |
|---|---|
| RSI SME owner (free tier) | Annual revenue 10M–50M XAF, uses the calculator a few times a month, price-sensitive |
| Tassi Plus subscriber | Same profile, has opted into reminders + history, pays a small recurring fee |

**Not yet served (v2.0):** micro-merchants under Régime Libératoire, businesses over 50M XAF/year (Régime Réel). See G1.

### 2.4 Operating Environment

- **Client:** WhatsApp on any smartphone
- **Server:** single VPS (EU region — see SDD §2 for the latency rationale), running FastAPI + Postgres + Redis
- **Scheduler:** OS cron / APScheduler in-process — no separate job queue

### 2.5 Constraints

- All monetary math uses Python `decimal`, never `float`
- Tax rate and CAC handling must be config-driven (see FR-TAX-1), not hardcoded, pending G1
- External integrations (Meta, Campay) must be treated as **AP** (Available, Partition-tolerant) — never block a user reply on an external call; reconcile asynchronously (SDD §3)
- The database is a **single Postgres instance** — no distributed-database trade-offs apply to it (SDD §3)

### 2.6 Assumptions & Dependencies

- Users have WhatsApp and basic French or English literacy
- Campay provides MTN MoMo / Orange Money collection (confirmed: flat 2% fee on collections)
- Meta's per-template pricing applies to any bot-initiated message — see FR-NOTIF for how this is contained

---

## 3. Validation Gates

These are open questions that gate specific requirements below. They are tracked here explicitly rather than assumed away.

| Gate | Question | Blocks | Resolution path |
|---|---|---|---|
| **G1** | Is the RSI Acompte = 5.5% × revenue, and is CAC an additional +10% or already included in that 5.5%? | FR-TAX-2 (showing a single "Total Owed" figure) | One consultation with a licensed Cameroonian tax professional |
| **G2** | Does charging for Tassi Plus constitute regulated fiscal-advisory activity requiring a license? | FR-SUB (charging at all) | One consultation with a Cameroonian business/consumer-law professional |
| **G3** | Will real users pay for Tassi Plus, and at what price? | FR-SUB-2 (price), FR-NOTIF-2 (Plus-only reminders) | Manual Wizard-of-Oz pilot (free WhatsApp app + spreadsheet) with ~20-30 real users over one filing cycle |

**Until G1 closes:** Tassi shows Base Acompte as a confirmed figure and CAC as a clearly-labeled unconfirmed figure (FR-TAX-2). It does not present a single blended "Total Owed" number.

**Until G2 closes:** Tassi Plus may be built and tested, but must not be marketed with compliance-guarantee language (e.g., "Penalty Shield").

**Until G3 closes:** FR-SUB ships with a placeholder price; FR-NOTIF-1 (free-tier reminder) ships, FR-NOTIF-2 (Plus-only reminders) is feature-flagged off.

---

## 4. Functional Requirements (FR)

### 4.1 Conversational Ingestion (FR-CHAT)

- **FR-CHAT-1:** Capture inbound Meta webhook payloads; use the sender's MSISDN as the user identifier. Create a `users` row on first contact.
- **FR-CHAT-2:** Maintain conversational state in Redis under `session:<msisdn>`, TTL 2 hours.
- **FR-CHAT-3:** Sanitize numeric input via regex (strip everything but digits) before casting to `Decimal`.
- **FR-CHAT-4:** Support French and English; default to French, switch on user's first message language or explicit command.
- **FR-CHAT-5:** If sanitization yields no digits, reply with a numeric-only prompt; do not advance session state.
- **FR-CHAT-6 (idempotency):** Deduplicate inbound webhooks on Meta's `message_id` (Redis `SETNX` with the ID as key, short TTL). A retried webhook for an already-processed message must not trigger a second reply or a second calculation row. *(Required because mobile network retries are routine in this environment — see SDD §3.)*

### 4.2 Tax Calculation (FR-TAX) — gated by G1

- **FR-TAX-1:** Compute `base_acompte = gross_revenue × RATE_RSI` (config value, default `0.055`), using `Decimal`, rounded to 2 places.
- **FR-TAX-2 (transparency until G1 closes):** Reply format is:
  > "Base Acompte (RSI 5.5%): XAF {base_acompte} — confirmed.
  > Possible CAC surcharge: XAF {base_acompte × 0.10} — **unconfirmed, ask your tax advisor whether this is additional or already included.**"

  Once G1 resolves, this collapses to a single confirmed total per `CAC_MODE` config (`ADDITIVE` | `INCLUDED`).
- **FR-TAX-3:** If sanitized revenue = 0, or input matches "néant"/"rien"/"nothing"/"0", route to the Déclaration Néant message (free, no calculation needed) instead of FR-TAX-1/2.
- **FR-TAX-4:** Persist every calculation to `tax_calculations` (user_id, gross_revenue, base_acompte, fiscal_period `YYYY-MM`, cac_mode_used, created_at) — this is the data Plus subscribers retrieve as "filing history."
- **FR-TAX-5 (onboarding sanity check):** At onboarding, ask the user's approximate annual revenue. If outside 10M–50M XAF, tell them Tassi currently only supports RSI and does not yet cover their bracket — do not proceed to FR-TAX-1. *(Prevents silently misapplying RSI math to Libératoire/Réel taxpayers — this was a real error in the v1.0 personas.)*

### 4.3 Tassi Plus Subscription (FR-SUB) — gated by G2, G3

- **FR-SUB-1:** A user may opt into "Tassi Plus" via a `SUBSCRIBE` command or button.
- **FR-SUB-2:** Price is a config value (placeholder until G3). Tassi Plus is **monthly, manually renewed** — see FR-PAY-4 (MoMo does not support silent auto-debit for small merchants).
- **FR-SUB-3:** Active Plus subscribers can send `HISTORY` to receive their last 12 `tax_calculations` rows as a formatted message.
- **FR-SUB-4:** Active Plus subscribers receive the Day-10 reminder (FR-NOTIF-2).
- **FR-SUB-5:** If the DGI Harmony portal's field layout changes (detected manually — see SDD §7), Plus subscribers are notified of the update; this is the "kept current" value that replaces the static one-off blueprint from v1.0.

### 4.4 Payments (FR-PAY)

- **FR-PAY-1:** `SUBSCRIBE` presents MTN MoMo / Orange Money as button options.
- **FR-PAY-2:** On selection, call Campay to trigger a USSD PIN prompt. Create a `payment_transactions` row with status `PENDING`.
- **FR-PAY-3 (AP pattern):** Do not block the chat session on the Campay webhook. On `SUCCESS` webhook, mark `SUCCESS`, activate/extend the subscription period, and send a confirmation message.
- **FR-PAY-4:** Provide a `STATUS` command that re-polls Campay for any transaction `PENDING` for >2 minutes — covers dropped webhook delivery (SDD §3).
- **FR-PAY-5:** 3 days before a Plus subscription period ends, send a renewal prompt (this is the "manual renewal," since recurring auto-debit isn't realistically available via MoMo for a small merchant).

### 4.5 Notifications (FR-NOTIF)

- **FR-NOTIF-1 (all users, acquisition hook):** On Day 14 of the fiscal month, send one reminder to every user who has used the calculator at least once this period: "Filing window closes tomorrow."
- **FR-NOTIF-2 (Plus only, feature-flagged off until G3):** On Day 10, send Plus subscribers an early reminder + prompt to log this month's figure.
- **FR-NOTIF-3:** Both reminders are sent via a single daily cron job querying active users — no separate job queue.

### 4.6 Data & Audit (FR-DATA)

- **FR-DATA-1:** Every calculation (FR-TAX-4) and payment state transition (FR-PAY) is append-only — no updates/deletes — forming a simple audit trail.
- **FR-DATA-2:** Nightly automated `pg_dump` to object storage, retained 30 days.
- **FR-DATA-3:** Per-MSISDN rate limit (`rate_limit:<msisdn>`, Redis, 60s TTL) to absorb accidental message loops.

---

## 5. Non-Functional Requirements (NFR)

### 5.1 Security & Privacy (NFR-SEC)

- **NFR-SEC-1:** No programmatic link to DGI systems.
- **NFR-SEC-2:** Revenue figures and PII encrypted at rest (Postgres column-level or disk-level encryption — full envelope/KMS design deferred until user volume justifies the operational overhead).
- **NFR-SEC-3:** All inbound Meta webhooks validated against Meta's signature header.
- **NFR-SEC-4:** Onboarding message states data is not shared with DGI.

### 5.2 Performance (NFR-PERF)

- **NFR-PERF-1:** Webhook acknowledged (`200 OK`) to Meta within 500ms.
- **NFR-PERF-2:** Calculation reply delivered within 1.2s end-to-end for the common case (no external calls on this path).

### 5.3 Availability (NFR-AVAIL)

- **NFR-AVAIL-1 (realistic target):** Single-VPS deployment; target is "recoverable within 1 hour" via the nightly backup (FR-DATA-2), not 99.9% uptime. This is stated honestly rather than inherited from a multi-instance design that doesn't exist yet.
- **NFR-AVAIL-2:** No code deploys during the 8th–16th of each month (peak filing window).
- **NFR-AVAIL-3 (degraded mode):** If Redis is unavailable, FR-TAX-1/2 (the free calculation — highest-value path) must still work; only session-state niceties (FR-CHAT-2) and rate limiting degrade.

### 5.4 Scalability (NFR-SCALE)

- **NFR-SCALE-1:** The FastAPI app is stateless (all session state in Redis), so a second instance behind a load balancer is an operational change, not a redesign, if/when needed.
- **NFR-SCALE-2:** No scaling work is justified below ~1,000 active users; vertical scaling of the single VPS covers growth until then.

### 5.5 Usability & Localization (NFR-USE)

- **NFR-USE-1:** Bilingual French/English.
- **NFR-USE-2:** Input tolerant of `1.500.000`, `1,500,000`, `1 500 000 frs`.
- **NFR-USE-3:** Zero-revenue reachable via a single quick-reply button.
- **NFR-USE-4 (`RESEND`):** Any user can send `RESEND` to get their most recent calculation again — addresses WhatsApp-history-clearing behavior common on storage-constrained devices.

### 5.6 Maintainability (NFR-MAINT)

- **NFR-MAINT-1:** `RATE_RSI`, `CAC_MODE`, `CAC_RATE`, and Plus pricing are environment-config values.
- **NFR-MAINT-2:** Ruff/Black/Pytest on every change; calculation rounding behavior has dedicated tests.

---

## 6. External Interfaces

| Interface | Provider | Purpose |
|---|---|---|
| WhatsApp Business Cloud API | Meta | Messaging, webhooks, buttons |
| Campay API | Campay | MTN MoMo / Orange Money collection (confirmed 2% fee) |

---

## 7. Data Requirements

| Entity | Purpose |
|---|---|
| `users` | MSISDN, language, declared annual revenue band, Plus status |
| `tax_calculations` | Append-only calculation history (free + Plus) |
| `subscriptions` | Plus period start/end, status |
| `payment_transactions` | Append-only payment ledger |
| `idempotency_log` (or Redis keys) | Dedup of inbound webhook message IDs |

Retention: indefinite for calculation/payment history (it's the Plus value proposition); session state TTL 2h.

---

## 8. Deferred / Out of Scope (and the trigger to revisit)

| Item | Revisit when |
|---|---|
| Régime Libératoire / Réel support | G1 resolved separately for those regimes |
| PostGIS / commune CAC table | Evidence of genuine commune-level CAC variance found |
| Admin web dashboard | Direct DB queries become impractical (>~few hundred users needing support) |
| Celery / job queue | Cron job demonstrably can't keep up (unlikely below 10k users) |
| Multi-instance / load balancer | Single VPS demonstrably saturated |
| Auto-renewing subscriptions | A MoMo aggregator offering real recurring billing is identified |
