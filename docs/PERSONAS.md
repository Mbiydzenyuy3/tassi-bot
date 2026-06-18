# Tassi User Personas & User Stories

**Version:** 2.1 (Pidgin zero-return phrases; FR-CHAT-7 mid-session language; FR-CHAT-8 typing indicator; is_plus as property)
**Based on:** Tassi SRS v2.1 / SDD v2.1
**Supersedes:** v1.0 (Florence Kamga / Jean-Pierre Atangana personas)

---

## 0. Why This Document Was Rewritten

The v1.0 personas put both users **outside the tax regime Tassi was supposedly calculating for them**:

- "Florence" had a monthly revenue of 4.5M–8M XAF (≈54M–96M XAF/year) — above the RSI ceiling of 50M XAF/year, which would actually put her in **Régime Réel** (2.2% Acompte, different mechanics entirely).
- "Jean-Pierre" had revenue up to 1.8M XAF/month (≈21.6M XAF/year) — above the **Régime Libératoire** ceiling of 10M XAF/year, so the "Déclaration Néant" walkthrough didn't match his actual obligations.

Both errors were silent — the bot in v1.0 would have applied the wrong formula to the wrong person with full confidence. **FR-TAX-5** exists precisely to catch this class of mistake at onboarding, and this document's two personas are deliberately written with revenues that fall cleanly inside the **RSI band (10M–50M XAF/year, i.e. roughly 833K–4.17M XAF/month)** — the only band v2.0 serves.

This document is the primary "how it works" reference for v2.0: read the two walkthroughs below to understand the full system behavior end-to-end. The SRS states *what* is required and the SDD states *how it's built*; this document shows *what the user experiences*, mapped back to the FR IDs that produce it.

---

## 1. How Tassi Works — Overview

Tassi is reached through a single WhatsApp number. There is no app to install. Every interaction is one of these:

```
First contact ──► Onboarding (language + revenue band check, FR-TAX-5)
                        │
                        ▼
            ┌── Free tier (everyone) ──────────────────┐
            │  • Send a number → get Base Acompte       │
            │    (confirmed) + CAC note (unconfirmed)   │
            │  • Send "0" / "rien" / "néant" →           │
            │    Déclaration Néant guidance              │
            │  • RESEND → repeat last calculation        │
            │  • Day-14 reminder (everyone who's used it)│
            └────────────┬───────────────────────────────┘
                          │ SUBSCRIBE
                          ▼
            ┌── Tassi Plus (paid, optional) ─────────────┐
            │  • Everything in free, plus:                │
            │  • HISTORY → last 12 months of calculations │
            │  • Day-10 reminder (earlier heads-up)        │
            │  • Notified if DGI Harmony portal changes    │
            └───────────────────────────────────────────┘
```

Two things are deliberately visible to the user, not hidden behind polish:

1. **The CAC figure is labeled "unconfirmed"** until Validation Gate G1 closes (SRS §3). Tassi would rather show a number with an honest caveat than a confident number that might be wrong.
2. **Payments feel like "processing…" rather than instant**, because Mobile Money confirmation webhooks aren't always reliable (SDD §3). The `STATUS` command exists for exactly this.

---

## 2. Persona 1 — Free Tier, First-Time User

**Aïssatou Bello**, 34, runs a wax-fabric and textile stall in the Bafoussam central market. Declared annual turnover is roughly **30M XAF/year** (~2.5M XAF/month) — comfortably inside the RSI band (10M–50M XAF/year). She has a basic Android phone, uses WhatsApp daily for supplier orders, and has never filed a return digitally before.

### Story 1.1 — First Contact & Onboarding (FR-CHAT-1, FR-TAX-5)

> **Aïssatou:** Bonjour

This is her first message to the Tassi number. Behind the scenes:

- **FR-CHAT-1:** Meta's webhook delivers the message; Tassi creates a `users` row keyed on her WhatsApp MSISDN.
- **FR-CHAT-4:** Her message is in French, so the conversation defaults to French (no language command needed).

> **Tassi:** Bonjour ! Je suis Tassi 🇨🇲, je vous aide à calculer votre Acompte mensuel.
> Pour commencer, quel est votre revenu annuel approximatif ?
> [Moins de 10M XAF/an]  [Entre 10M et 50M XAF/an]  [Plus de 50M XAF/an]

> **Aïssatou:** *(taps)* Entre 10M et 50M XAF/an

- **FR-TAX-5:** Her answer sets `users.annual_revenue_band = 'RSI_10_50M'`. Because this falls inside the RSI band Tassi supports, the bot proceeds. *(Had she tapped "Moins de 10M" or "Plus de 50M", she'd see a polite message that Tassi doesn't yet cover her bracket — see Edge Case E4.)*

> **Tassi:** Parfait. Chaque mois, envoyez-moi votre chiffre d'affaires (revenu brut) du mois, et je calcule votre Acompte. Quel est votre revenu pour ce mois ?

### Story 1.2 — Messy Input & The Transparent Calculation (FR-CHAT-3, FR-TAX-1, FR-TAX-2, FR-TAX-4)

> **Aïssatou:** 2.350.000 frs

This is realistic — Cameroonian users commonly write large numbers with `.` or `,` as thousand separators, plus a currency suffix.

- **FR-CHAT-3:** The bot strips everything except digits → `2350000`, cast to `Decimal("2350000.00")`.
- **FR-TAX-1:** `base_acompte = 2,350,000.00 × 0.055 = 129,250.00` (rounded to 2 decimals, `Decimal` arithmetic throughout — SRS §2.5).
- **FR-TAX-2 (transparency reply, active because G1 is still open):**

> **Tassi:**
> 📊 **Votre Acompte — Octobre 2026**
>
> Acompte de base (RSI 5,5 %) : **XAF 129 250** — *confirmé*
>
> Majoration CAC possible : XAF 12 925 — *non confirmé. Demandez à votre conseiller fiscal si ce montant s'ajoute ou est déjà inclus dans l'Acompte de base.*
>
> ℹ️ Envoyez RESEND pour revoir ce calcul. Envoyez ABONNEMENT pour découvrir Tassi Plus (rappels + historique 12 mois).

- **FR-TAX-4:** This calculation is written to `tax_calculations` (append-only) with `cac_mode_used = 'UNCONFIRMED'`, `fiscal_period = '2026-10'`. If G1 later resolves to, say, `ADDITIVE`, this historical row still honestly records what Tassi told her *at the time* — it isn't silently rewritten.

Notice what Tassi does **not** do: it does not say "You owe XAF 142,175." It gives her the one number it's confident about, and is explicit about the one it isn't — because presenting a wrong number with false confidence is worse than admitting uncertainty (this was a core conclusion from the project's critical review).

### Story 1.3 — A Slow Month, Déclaration Néant (FR-TAX-3)

A month later, business was slow and she made no sales.

> **Aïssatou:** rien ce mois

- **FR-TAX-3:** The bot recognizes "rien" (along with "néant", "nothing", "0") as a zero-revenue declaration and routes to the Néant message *without* running FR-TAX-1/2 — there's nothing to calculate.

> **Tassi:** Compris — aucune vente ce mois-ci. Vous devez quand même soumettre une **Déclaration Néant** (déclaration à zéro) sur le portail DGI Harmony avant la date limite. [Voir comment faire →]
>
> Cette déclaration est gratuite et sera aussi enregistrée dans votre historique si vous passez à Tassi Plus.

### Story 1.4 — Day 14 Reminder (FR-NOTIF-1)

On the 14th of the month, because she's used the calculator at least once this fiscal period, a single daily cron job (SDD §8) includes her in its run:

> **Tassi:** ⏰ Rappel : la fenêtre de déclaration se ferme demain. Envoyez votre chiffre d'affaires de ce mois pour calculer votre Acompte, ou répondez "rien" si vous n'avez pas eu de ventes.

This is the **only** proactive message a free-tier user receives — and it's also Tassi's main acquisition hook for Tassi Plus, which adds an *earlier* (Day-10) version of this nudge.

---

## 3. Persona 2 — Tassi Plus Subscriber

**Robert Mballa**, 41, runs a small electronics and phone-accessories shop in Douala (Akwa). Monthly revenue is around **3.2M XAF** (~38.4M XAF/year — also inside the RSI band). He's been using Tassi's free calculator for two months and finds it useful enough to want the reminder + history features.

### Story 2.1 — Subscribing to Tassi Plus (FR-SUB-1, FR-SUB-2, FR-PAY-1)

> **Robert:** ABONNEMENT

- **FR-SUB-1:** This command starts the subscription flow.

> **Tassi:** **Tassi Plus** — XAF 500/mois *(tarif de lancement, peut évoluer)* :
> ✅ Rappel anticipé le 10 du mois
> ✅ Historique des 12 derniers mois
> ✅ Alerte si le format du portail DGI Harmony change
>
> Choisissez votre mode de paiement :
> [MTN Mobile Money]  [Orange Money]

- **FR-SUB-2:** The price shown (`XAF 500`) is a **placeholder config value** — Gate G3 (SRS §3) hasn't closed yet, so this number is explicitly flagged internally as provisional and may change based on the Wizard-of-Oz pilot results. The subscription itself is **monthly and manually renewed** (see Story 2.4) — there's no silent recurring debit.

### Story 2.2 — Payment, the "Processing…" Reality, and STATUS (FR-PAY-2, FR-PAY-3, FR-PAY-4)

> **Robert:** *(taps)* MTN Mobile Money

- **FR-PAY-2:** Tassi creates a `payment_transactions` row with `status = 'PENDING'` and calls Campay, which triggers a USSD PIN prompt on Robert's phone.

> **Tassi:** 📲 Vérifiez votre téléphone et entrez votre code MTN MoMo pour confirmer le paiement de XAF 500.
> *Traitement en cours — si vous ne recevez pas de confirmation dans 2 minutes, envoyez STATUS.*

- **FR-PAY-3 (AP pattern, SDD §3):** Tassi does **not** sit waiting for Campay. The chat is free to do other things while the payment resolves asynchronously.

Robert enters his PIN and approves the payment. But his connection drops for a few seconds right after — a routine occurrence — and **Campay's confirmation webhook never arrives**. Three minutes pass with no message from Tassi.

> **Robert:** STATUS

- **FR-PAY-4:** This command makes Tassi actively poll Campay for the `PENDING` transaction's real status (rather than passively waiting for a webhook that may never come). Campay reports the payment actually succeeded.

> **Tassi:** ✅ Paiement confirmé ! Tassi Plus est actif jusqu'au 14 novembre 2026. Bienvenue 🎉
> Envoyez HISTORIQUE à tout moment pour voir vos calculs précédents.

Internally: `payment_transactions.status → 'SUCCESS'`, a `subscriptions` row is created/extended (`period_start = today`, `period_end = today + 1 month`), and `users.is_plus = true`. This is the AP/reconciliation pattern from SDD §3 working as designed — the user experience is "a short delay, resolved by one command," not "the payment silently vanished."

### Story 3 — A Retried Message Doesn't Double-Count (FR-CHAT-6)

The following week, Robert sends his monthly revenue figure right as his phone loses signal:

> **Robert:** 3 200 000

His phone's WhatsApp app, unsure whether the message went through, has it redelivered by Meta a few seconds later — **same `message_id`, sent twice.**

- **FR-CHAT-6:** On the first delivery, Tassi runs `SETNX seen_msg:<message_id>` in Redis — it succeeds, so Tassi processes normally: calculates, replies, and writes one row to `tax_calculations`. On the second (retried) delivery, the same `SETNX` **fails** (the key already exists) — Tassi acknowledges Meta's webhook with `200 OK` but does **nothing else**. Robert sees exactly **one** reply and has exactly **one** entry in his history, even though the network delivered the message twice.

### Story 3.1 — HISTORY (FR-SUB-3)

> **Robert:** HISTORIQUE

> **Tassi:** 📅 **Vos 12 derniers calculs (Tassi Plus)**
>
> Oct 2026 — CA: XAF 3 200 000 → Acompte base: XAF 176 000
> Sep 2026 — CA: XAF 2 900 000 → Acompte base: XAF 159 500
> Aug 2026 — Déclaration Néant
> ... *(9 more rows)*

- **FR-SUB-3:** This pulls Robert's last 12 `tax_calculations` rows — the same append-only data every user (free or Plus) already generates via FR-TAX-4. Tassi Plus doesn't compute anything new here; it just makes the existing history retrievable. This is the "kept current, recurring value" Tassi Plus is built around (replacing v1.0's one-off static blueprint, which had nothing left to offer after the first read).

### Story 3.2 — Day-10 Reminder (FR-NOTIF-2 — feature-flagged off until G3)

*(Described here for completeness — this feature is currently OFF in production pending Gate G3's pricing/demand validation, per SRS §3.)*

Once enabled, on the 10th of each month the same daily cron job that sends the Day-14 reminder to everyone (Story 1.4) will additionally message Plus subscribers:

> **Tassi:** 👋 Rappel anticipé Tassi Plus : pensez à enregistrer votre chiffre d'affaires d'octobre dès que possible pour rester en avance sur la date limite.

### Story 3.3 — Renewal Prompt (FR-PAY-5)

Three days before Robert's subscription period ends (so, 11 November 2026 for a period ending 14 November):

> **Tassi:** Votre abonnement Tassi Plus expire dans 3 jours (14 novembre). Pour continuer à recevoir vos rappels et votre historique, envoyez RENOUVELER.

Because MoMo doesn't support silent recurring debits for a merchant at this scale (SRS §4.3), every renewal is this same one-tap manual flow — Tassi is explicit about this rather than implying "auto-renewal" and disappointing users when it doesn't happen.

---

## 4. Edge Cases

| # | Scenario | Tassi's Behavior | Requirement(s) |
|---|---|---|---|
| E1 | User sends revenue with mixed formatting (`1.500.000`, `1,500,000`, `1 500 000 frs`, emoji, typos) | Regex strips all non-digit characters before casting to `Decimal`; if zero digits remain, ask again without advancing state | FR-CHAT-3, FR-CHAT-5, NFR-USE-2 |
| E2 | Same WhatsApp message delivered twice (mobile network retry) | Second delivery is acknowledged but produces no second reply and no duplicate `tax_calculations` row (Redis `SETNX` on `message_id`) | FR-CHAT-6 |
| E3 | User reports zero revenue — numeric `0`; French: "rien", "néant"; English: "nothing", "nada"; Pidgin: "e no get", "no money", "e finish", "nothing dey", "i no sell" | Routed directly to Déclaration Néant guidance; no Acompte calculation performed | FR-TAX-3 |
| E4 | At onboarding, user's annual revenue is outside 10M–50M XAF | Bot states Tassi currently only supports the RSI band and does not proceed to calculations; user is not silently given an RSI-based figure that doesn't apply to them | FR-TAX-5 |
| E5 | User asks "so what's my total?" / wants one number instead of two | Bot repeats the FR-TAX-2 transparency format (confirmed base + unconfirmed CAC) and explains *why* — it does not fabricate a blended total while G1 is open | FR-TAX-2, G1 |
| E6 | Campay's payment-success webhook never arrives after a real successful MoMo payment | User sends `STATUS`; Tassi polls Campay directly, finds the true status, and updates the transaction/subscription accordingly | FR-PAY-4, SDD §3 |
| E7 | User's WhatsApp history was cleared (common on low-storage devices) and they've lost their last result | User sends `RESEND`; Tassi re-sends their most recent `tax_calculations` entry in the FR-TAX-2 format | NFR-USE-4 |
| E8 | User switches between French, English, or Pidgin mid-conversation (code-switching is common in Cameroon) | Bot auto-detects the language of each incoming message (FR-CHAT-7) and replies in kind. Numeric-only input inherits the last detected language. Typing indicator (FR-CHAT-8) is sent before every reply. | FR-CHAT-4, FR-CHAT-7, FR-CHAT-8, NFR-USE-1 |
| E9 | A user sends many messages in quick succession (accidental loop / spam) | Per-MSISDN Redis rate limit (`rate_limit:<msisdn>`, 60s TTL) absorbs the burst | FR-DATA-3 |
| E10 | Redis is temporarily unavailable | The core calculation path (FR-TAX-1/2) still works using stateless request data; only session continuity and rate limiting degrade | NFR-AVAIL-3 |
| E11 | Tassi Plus subscription expires without renewal | `subscriptions.status → 'EXPIRED'`; user reverts to free-tier behavior (no HISTORY, no Day-10 reminder) but free-tier features (FR-TAX-1/2/3) continue uninterrupted | FR-SUB-2 |

---

## 5. Test Scenarios / Acceptance Checklist

| ID | Scenario | Steps | Expected Result | Maps to |
|---|---|---|---|---|
| T1 | First-contact onboarding, in-band | New MSISDN sends any message → selects "Entre 10M et 50M XAF/an" | `users` row created; `annual_revenue_band = 'RSI_10_50M'`; bot proceeds to ask for monthly revenue | FR-CHAT-1, FR-TAX-5 |
| T2 | First-contact onboarding, out-of-band | New MSISDN selects "Moins de 10M" or "Plus de 50M" | Bot explains Tassi doesn't cover this bracket yet; does **not** proceed to a calculation | FR-TAX-5 |
| T3 | Messy-input calculation | Send `"2.350.000 frs"` after onboarding | Reply shows Base Acompte = XAF 129,250.00 (confirmed) + CAC = XAF 12,925.00 (unconfirmed); `tax_calculations` row written with `cac_mode_used='UNCONFIRMED'` | FR-CHAT-3, FR-TAX-1, FR-TAX-2, FR-TAX-4 |
| T4 | Zero-revenue declaration | Send `"rien"` | Déclaration Néant guidance returned; no `tax_calculations` row with a non-null `base_acompte` (or `is_zero_return=true` row, per schema) | FR-TAX-3 |
| T5 | Duplicate webhook delivery | Replay an identical webhook payload (same `message_id`) within the dedup TTL | Second request returns `200 OK` to Meta; no second reply sent; `tax_calculations` row count unchanged | FR-CHAT-6 |
| T6 | RESEND | After T3, send `"RESEND"` | Bot re-sends the exact T3 result | NFR-USE-4 |
| T7 | Subscribe + successful webhook | `ABONNEMENT` → select MTN MoMo → Campay sends `SUCCESS` webhook promptly | `payment_transactions.status='SUCCESS'`, `subscriptions` row created with `status='ACTIVE'` and future `period_end`; `user.is_plus` property returns `True`; confirmation sent | FR-SUB-1, FR-PAY-1, FR-PAY-2, FR-PAY-3 |
| T8 | Subscribe + dropped webhook + STATUS | Same as T7, but suppress the Campay webhook; after 2+ minutes send `STATUS` | Tassi polls Campay, discovers `SUCCESS`, updates state identically to T7 | FR-PAY-4 |
| T9 | HISTORY for Plus subscriber | As a Plus user with ≥1 prior calculation, send `HISTORIQUE`/`HISTORY` | Bot returns up to the last 12 `tax_calculations` rows, newest first | FR-SUB-3 |
| T10 | HISTORY for free user | As a non-Plus user, send `HISTORIQUE`/`HISTORY` | Bot prompts to subscribe to Tassi Plus; does not return calculation history | FR-SUB-1, FR-SUB-3 |
| T11 | Day-14 reminder | Run the daily cron with system date = 14th | Every user with ≥1 calculation this fiscal period receives the Day-14 message exactly once | FR-NOTIF-1, FR-NOTIF-3 |
| T12 | Day-10 reminder (flagged off) | Run the daily cron with system date = 10th, `FEATURE_PLUS_REMINDERS_ENABLED=false` | No Day-10 messages sent, to anyone | FR-NOTIF-2 (gated by G3) |
| T13 | Renewal prompt | A Plus subscription's `period_end` is 3 days away; run the daily cron | Affected user receives the renewal prompt exactly once | FR-PAY-5 |
| T14 | Rate limiting | Send >N messages from one MSISDN within 60 seconds | Excess messages beyond the configured limit are acknowledged (`200 OK`) but not individually processed/replied to | FR-DATA-3 |
| T15 | Redis-down degraded mode | Stop Redis; send a valid revenue figure as a returning user | FR-TAX-1/2 calculation still returns correctly; only session-state-dependent niceties are affected | NFR-AVAIL-3 |
| T16 | Rounding correctness | Run `tax.py` unit tests across revenue values that produce non-trivial rounding (e.g., `1234567.89`) | All amounts use `Decimal`, rounded to exactly 2 places, matching expected fixtures | NFR-MAINT-2 |
| T17 | Config-driven rate change | Change `RATE_RSI` or `CAC_MODE` in environment config and restart | New calculations use the new values immediately; no code change required; historical rows retain their original `cac_mode_used` | NFR-MAINT-1, FR-TAX-4 |
