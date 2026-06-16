# Tassi — Capacity, Security & Architecture Assessment

**Version:** 1.0
**Tone:** Brutally honest. No vanity metrics, no wishful thinking.
**Purpose:** Ground-truth reference for how many users this can serve, what security it provides, and how solid the foundation actually is — with explicit gaps and how to close them.

---

## 1. User Capacity — Honest Estimation

### 1.1 Total Addressable Market (TAM)

Before projecting users, the honest ceiling has to be established.

**Cameroonian registered RSI businesses (the only segment v2.0 serves):**

| Estimate | Source basis |
|---|---|
| ~600,000–800,000 total registered taxpayers (all regimes) | DGI public reports, approximate |
| ~100,000–200,000 businesses plausibly in RSI range (10M–50M XAF/year) | Derived from regime distribution; no public per-regime breakdown exists |
| ~70–80% of those have WhatsApp | Cameroon smartphone + WhatsApp penetration; anecdotal confirmation from market |
| **Realistic reachable market: ~70,000–160,000 RSI businesses on WhatsApp** | — |

That is the ceiling. Getting 5% of it — 3,500 to 8,000 users — would be a genuinely strong outcome in Year 2. Getting 1% — 700 to 1,600 users — is a realistic Year 1 target after public launch.

The numbers above are estimates. There is no publicly available breakdown of Cameroonian businesses by tax regime at SME scale. Until the Wizard-of-Oz pilot runs (Gate G3), every projection below is informed guesswork, not fact.

---

### 1.2 Adoption Phase Projections

| Phase | Monthly Active Users | What drives it | What kills it |
|---|---|---|---|
| **Alpha (Months 1–2)** | 20–100 | Friends, family, controlled beta | Bugs, unclear onboarding |
| **Beta / Pilot (Months 3–5)** | 100–500 | Accountant referrals, SME WhatsApp groups, word of mouth | Trust ("will this get me audited?"), messy UX |
| **Post-G3 public launch (Months 6–9)** | 500–2,000 | Plus tier live, Day-10 reminders on, referral loop working | G3 fails (nobody pays), DGI anxiety kills trust |
| **Year 2 (sustainable growth)** | 2,000–10,000 | Organic growth, possible partnerships (accountants, MFIs) | Platform risk (Meta account suspension), competitor copies the bot |
| **Year 3+ (if product-market fit confirmed)** | 10,000–50,000 | Partnership channels, possibly Régime Libératoire added | Regulatory change, G1 stays unresolved too long |

**Honest reality check on Month 1:** Unless you already have a warm audience (an accountants' network, an SME association, a personal social following in the target community), Month 1 will be 20–50 users, mostly people you know personally. That is normal and expected. The Wizard-of-Oz pilot *is* Month 1. Don't build production infrastructure for 10,000 users until 200 real users have used it.

---

### 1.3 What the Architecture Can Actually Handle

This is where the honest good news is: the current single-VPS design is over-specced for the realistic near-term user base.

**Rough traffic model at 10,000 MAU:**
- Average user: 5–10 WhatsApp messages/month (calculation + follow-up + reminder response)
- Total webhook events/month: ~50,000–100,000
- Per day (spread across month): ~1,600–3,300 events/day
- Peak: 10th–15th filing window concentrates ~50% of monthly traffic into 5 days → ~5,000–10,000 events/day at peak → ~6–12 events/second at absolute peak
- A single FastAPI worker handles hundreds of requests/second under I/O-bound load. **The app is not the bottleneck at this scale.**

**Database load at 10,000 MAU:**
- ~10,000 rows/month added to `tax_calculations`
- `users` table: 10,000 rows — trivially small
- PostgreSQL on a 2-CPU/4GB VPS handles thousands of transactions/second. No issue until ~500,000 MAU.

**Redis load:**
- Session keys: ~2,000–3,000 active sessions at any time (2h TTL, not all users active simultaneously)
- Idempotency keys: burst of a few thousand per day at peak
- Negligible on any modern Redis instance

**Honest scaling ceiling before architecture change is needed:**
- Single VPS: comfortable to ~50,000 MAU, vertical resize covers to ~100,000 MAU
- First scaling intervention needed: read replica + second FastAPI instance, at ~100,000 MAU (see SDD §12)
- This is a good problem to have and years away at realistic adoption pace

---

### 1.4 What Will Actually Limit User Growth (Not Architecture)

The architecture will not be the constraint. These will be:

1. **Trust** — "Will typing my revenue into WhatsApp get me audited?" This fear is rational (see [docs/app.md §2.4](#24-the-dgi-data-risk-the-one-risk-you-cannot-engineer-away)). Overcoming it requires a clear, honest privacy message at onboarding and a track record of not sharing data.

2. **Awareness** — There is no app store. Discovery is entirely through word of mouth, SME WhatsApp groups, accountant referrals, and social media. Growth will be slow and social until a deliberate distribution strategy is in place.

3. **Filing literacy** — A significant portion of the target market doesn't file at all, either from ignorance or because their accountant handles it. Tassi assumes the owner is directly engaged with their filing. Not all are.

4. **Mobile data cost** — WhatsApp messages are cheap but not free. Some users on the lowest data bundles will be price-sensitive about a tool that sends them proactive messages.

5. **Platform dependency** — Tassi's entire distribution and delivery channel is controlled by Meta. A WhatsApp Business account suspension, policy change, or rate-limit adjustment ends the product immediately. This is not an engineering problem. It is a business risk with no technical solution.

---

## 2. Security

### 2.1 What Is Already In Place

| Control | Where | Status |
|---|---|---|
| `.env` gitignored | `.gitignore` | ✅ Live |
| `detect-private-key` pre-commit hook | `.pre-commit-config.yaml` | ✅ Live |
| Conventional commits + no-commit-to-main hook | `.pre-commit-config.yaml` | ✅ Live |
| All credentials are environment variables | `tassi/config.py` | ✅ Live |
| Non-root user in Docker runtime | `Dockerfile` | ✅ Live |
| Locked dependency versions (`uv.lock`) | repo root | ✅ Live |
| Dependabot for dep/action/Docker updates | `.github/dependabot.yml` | ✅ Live |
| CI blocks merge on lint/type/test failure | `.github/workflows/ci.yml` | ✅ Live |
| Code freeze 8th–16th of each month | `SRS NFR-AVAIL-2`, `CONTRIBUTING.md` | ✅ Policy |
| Nightly `pg_dump` to object storage (30 days) | `SRS FR-DATA-2` | Specified — not yet wired |
| Meta webhook signature verification | `SRS NFR-SEC-3` | Specified — not yet coded |
| Revenue data encrypted at rest | `SRS NFR-SEC-2` | Specified — not yet configured |
| Per-MSISDN rate limiting | `SRS FR-DATA-3` | Specified — not yet coded |
| Idempotency on `message_id` | `SRS FR-CHAT-6` | Specified — not yet coded |
| Redis session data contains no raw revenue figures | design intent | Enforced when `chat.py` is written |

---

### 2.2 Transport Security

**HTTPS / TLS**
Every request between Meta and the server, and between the server and Campay, is over HTTPS. This is not optional — Meta will not deliver webhooks to non-HTTPS endpoints. The TLS certificate is provisioned at the reverse proxy level (Nginx + Let's Encrypt on the VPS), not in the FastAPI app.

**Meta webhook signature verification (must be implemented before go-live)**

Every inbound webhook from Meta includes an `X-Hub-Signature-256` header:
```
X-Hub-Signature-256: sha256=<HMAC-SHA256(raw_body, META_APP_SECRET)>
```

The FastAPI webhook handler must verify this before processing any payload. If this check is missing, any actor who knows your webhook URL can send fake messages and trigger calculations, payments, or session state changes on behalf of real users. **This is the single most critical security control to implement on the first feature branch.**

```python
import hashlib, hmac

def verify_meta_signature(raw_body: bytes, signature_header: str, app_secret: str) -> bool:
    expected = "sha256=" + hmac.new(
        app_secret.encode(), raw_body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature_header)
```

`hmac.compare_digest` is mandatory — a plain `==` comparison is vulnerable to timing attacks.

---

### 2.3 Application Security

**Input sanitization**
All user-supplied text is treated as untrusted. Revenue figures are stripped to digits only before any numeric operation (FR-CHAT-3). No user input is ever interpolated into a SQL string — all queries go through SQLAlchemy's ORM or parameterized statements. No `f"SELECT ... WHERE id = {user_input}"` anywhere, ever.

**Rate limiting**
Per-MSISDN rate limiting via Redis prevents accidental message loops and deliberate abuse. A user who sends 20 messages in 60 seconds is throttled — the excess webhook calls are acknowledged to Meta (200 OK, so Meta stops retrying) but not processed.

**Idempotency**
The `seen_msg:<message_id>` Redis key (FR-CHAT-6) ensures that Meta's routine retries — or a user resending the same message after a network drop — never produce a duplicate calculation row, duplicate payment charge, or duplicate WhatsApp reply. This must be implemented before the first real user touches the system.

**No admin interface exposed to the internet**
There is no web admin dashboard (explicitly deferred in SRS §8). Database access is via direct SSH tunnel to the VPS. This eliminates an entire class of authentication vulnerabilities.

**Campay payment webhook verification**
Campay payment result webhooks must also be verified — check Campay's signature or shared-secret mechanism in their API documentation before implementing `payments.py`. A forged Campay webhook saying "payment succeeded" would activate Tassi Plus without actual payment.

---

### 2.4 Data Security

**Encryption at rest**
Revenue figures and MSISDNs are personal financial data. The minimum acceptable control is disk-level encryption at the VPS provider (most managed providers offer this at no extra cost). The stronger control — `pgcrypto` column-level encryption on `gross_revenue` and `base_acompte` in `tax_calculations` — should be added when the models are written on the first feature branch. It adds marginal complexity but means that even a compromised Postgres dump reveals no usable revenue data without the encryption key.

**What is never stored in Redis**
Redis session state (`session:<msisdn>`) tracks conversation step and language only. It never contains raw revenue figures, payment references, or personally identifiable data beyond the MSISDN (which is already the key). If Redis is compromised or its contents are logged, no financial data is exposed.

**Retention limits**
The SRS currently says "indefinite" for calculation history (it is the Plus value proposition). This needs revisiting. Indefinite retention of user financial records creates indefinite liability — legal discovery risk, breach exposure, and potential regulatory issues. A reasonable default: retain `tax_calculations` rows for 36 months, then archive to encrypted cold storage or delete. This is a product decision, but it should be made explicitly, not by omission.

**Backup security**
The nightly `pg_dump` is useless if the backup itself is unencrypted and accessible to anyone with the object storage credentials. Backups must be GPG-encrypted before upload. The decryption key lives only in an offline location (password manager, not on the VPS). An unencrypted backup of financial data sitting in S3-compatible storage is a breach waiting to happen.

---

### 2.5 The DGI Data Risk — The One Risk You Cannot Engineer Away

This deserves its own section because no amount of encryption or rate-limiting addresses it.

Users input their monthly gross revenue into Tassi. They believe this data stays with Tassi. If Cameroonian law enforcement or DGI issues a lawful data request, Tassi is legally obligated to comply. The data you hold on each user is:
- Their MSISDN (identity)
- 12 months of self-reported monthly revenue
- Filing behaviour and consistency

If a user declared XAF 3.2M/month to Tassi but filed XAF 1.8M/month with DGI, Tassi's database is evidence of that discrepancy. The user had no idea they were creating this record when they sent a WhatsApp message to a tax calculator.

**The only engineering mitigations are:**
1. Encrypt all revenue data at rest so that a database dump alone is not readable
2. Have a documented data retention and deletion policy — data that no longer exists cannot be subpoenaed
3. Have a legal process policy before you have real users — what happens when you receive a government data request?

**The non-engineering mitigation is the most important one:**
Onboarding message must state, in plain language in French: *"Vos données ne sont pas partagées avec la DGI ou toute autre autorité. Elles sont stockées de manière sécurisée et utilisées uniquement pour calculer votre Acompte."*

If you cannot make that statement honestly and permanently, you should not collect the data.

---

### 2.6 Supply Chain Security

- **`uv.lock` is committed.** Every CI run and production deployment installs exactly the pinned versions. A compromised upstream package cannot silently slide into a production deploy.
- **Dependabot** opens weekly PRs for dependency updates. These must be reviewed — not auto-merged — especially for `fastapi`, `sqlalchemy`, and `pydantic-settings`, which have breaking changes between major versions.
- **GitHub Actions** are pinned to specific versions (`actions/checkout@v4`) to prevent a compromised action from injecting malicious steps into the pipeline. When Dependabot proposes action updates, verify the SHA before merging.

---

## 3. Architecture Solidity

### 3.1 What Is Genuinely Strong

**Single-node simplicity eliminates distributed systems failure modes.**
Every system that adds nodes, replicas, message brokers, or service meshes adds new failure modes. Tassi's v2.0 architecture has one FastAPI process, one Postgres instance, one Redis instance, on one VPS. When something breaks, there is only one place to look. The operational burden on a solo or small team is manageable. This is not a weakness disguised as a strength — it is the right choice for this stage and this team size.

**Stateless application layer.**
The FastAPI app holds zero state in memory. All session state is in Redis; all durable data is in Postgres. This means a process restart or a container redeploy loses nothing. It also means adding a second instance behind a load balancer is an operational change, not an architectural change — when that day comes (SDD §12).

**Idempotency at the right boundaries.**
The AP pattern at Meta and Campay boundaries (SDD §3) is correctly designed. These are the two places in the system where real-world network partitions happen routinely in Cameroon. The `message_id` dedup and the `STATUS` command reconciliation are the right solutions to the right problems.

**Config-driven tax engine.**
When Gate G1 resolves — whether CAC is additive or included — the change is a single environment variable update and a server restart, not a code change, not a deployment, not a database migration. This is the correct design for a variable that is both legally significant and currently uncertain.

**Append-only financial records.**
`tax_calculations` and `payment_transactions` are never updated or deleted in normal operation. This provides a natural audit trail, eliminates a class of data corruption bugs, and makes the history query for Plus subscribers trivially correct.

**Migration-controlled schema.**
Alembic handles every schema change. There are no ad-hoc `ALTER TABLE` commands executed directly on the production database. Every change is versioned, reversible (within reason), and reproducible in CI.

---

### 3.2 What Is Fragile — Honest Assessment

**The VPS is a single point of failure.**
If the VPS provider has an outage, Tassi is down. If the disk fails, Tassi is down until the backup is restored. The SRS honestly states the RTO as "recoverable within 1 hour" — which means up to 1 hour of downtime. If this happens on the 14th of the month (the day before the filing deadline), users who haven't filed yet cannot use the tool at the worst possible moment.

There is no engineering solution to this at current scale that isn't more expensive and complex than the problem warrants. The mitigation is: reliable nightly backup, tested restore procedure (do a restore drill monthly — not just assuming it works), and an uptime monitoring alert to know about the outage fast.

**Meta can suspend the WhatsApp Business account without notice.**
This has happened to other businesses. Meta's enforcement is automated and opaque. A spike in user complaints, a message template flagged as spam, or an automated policy violation can take the account offline. When this happens, Tassi is completely non-functional — there is no fallback channel.

There is no engineering solution to this either. Mitigations: keep message templates conservative and clearly compliant, respond to Meta support quickly, have a secondary contact channel (SMS or email) ready for users even if it's never used.

**Campay is a small company.**
If Campay's API goes down, the Tassi Plus subscription flow is broken. If Campay goes out of business, the payment flow needs a complete rewrite. Campay has been the right choice given confirmed 2% fee and MoMo integration, but the dependency concentration is real. The `payments.py` module should be designed with an abstraction layer that makes swapping payment processors a contained change.

**The Wizard-of-Oz pilot has not happened yet.**
The entire Plus tier — subscription, payments, HISTORY command, Day-10 reminders, renewal prompts — is built on the assumption that real users will pay for it at some price. Gate G3 is open. If the pilot reveals that users won't pay, the Plus tier needs to be redesigned. Any code written for Plus before G3 closes is code that may need to be thrown away.

**DGI Harmony portal changes are detected manually.**
One person, once a month, checks whether the DGI Harmony portal's field layout has changed. If they forget, or are sick, or miss a change, Plus subscribers receive incorrect line-mapping information. This is acceptable at 100 Plus users. It is not acceptable at 5,000 Plus users. Automated portal monitoring (a headless browser check, a simple hash comparison of known page elements) should be on the backlog for when the Plus user count justifies it.

**There is no operational runbook yet.**
What does the on-call person do when the VPS goes down at 2am on the 14th? What is the exact sequence of steps to restore from backup? Who has the VPS credentials? Who has the Campay dashboard login? Where is the GPG decryption key for the backup? None of this is documented. A system that works in normal operation but has no runbook for failure is fragile regardless of how well the code is written.

---

### 3.3 How to Achieve and Maintain Solidity

These are ordered by priority. The first three must be done before the first real user:

**1. Implement Meta webhook signature verification first, before any other feature.**
No other code matters if forged webhooks can manipulate the system.

**2. Test the backup restore procedure before go-live.**
Run `pg_dump`, encrypt it, upload it, then restore it to a clean Postgres instance and verify the data is intact. Do this once before launch. Schedule it monthly after. Write down the steps.

**3. Write the operational runbook.**
One markdown file (not in the public repo if it contains VPS IPs and credential locations): what to do when the VPS is down, when the Campay webhook stops arriving, when Meta suspends the account, when a user reports a wrong calculation. This document does not need to be long. It needs to exist.

**4. Add uptime monitoring before the first public user.**
UptimeRobot free tier (5-minute checks) against the `/health` endpoint sends an SMS or email alert within minutes of the VPS going down. This costs nothing and means the outage is discovered fast rather than by a user complaint.

**5. Run the Wizard-of-Oz pilot before writing Plus code.**
20–30 real RSI business owners, one filing cycle, manual calculation via spreadsheet, manual WhatsApp responses. This validates: Does the tax formula work for real users? Does the onboarding question about revenue band work? Will users pay for Plus? What price? What is the actual biggest friction point? The answers change what gets built. Do not skip this step.

**6. Write `chat.py` with webhook signature verification, rate limiting, and idempotency as non-negotiable first-pass requirements** — not afterthoughts to be added in a second PR. These three controls are load-bearing. The feature branch that adds the conversation flow must ship all three or it does not merge.

**7. Encrypt revenue columns in Postgres when models are written.**
Add `pgcrypto` extension and encrypt `gross_revenue` and `base_acompte` at the column level. The application-layer key lives in `config.py` as an environment variable. This adds one line of complexity per write/read and provides meaningful protection if the database is ever dumped by an attacker.

**8. Design `payments.py` with a payment provider abstraction.**
A thin interface (`collect(amount, msisdn, method)` → `PaymentResult`) means swapping from Campay to another provider is a contained change. Don't hard-code Campay's API shape into the rest of the application.

**9. Enforce the 8th–16th code freeze as a hard rule, not a suggestion.**
This is the period when an outage is most damaging. The CI/CD pipeline could be configured to block deployments to production during this window automatically (environment protection rules in GitHub Actions, a calendar-based condition). It is currently a policy. Make it mechanical.

**10. Document the data retention policy before public launch.**
Decide the maximum age of `tax_calculations` rows, the backup retention period beyond 30 days, and the answer to "what happens to my data if I ask you to delete it?" Put this in the onboarding message and in the privacy notice. Not in legalese — in a WhatsApp message a market trader in Bafoussam can understand.

---

## 4. Summary Scorecard

| Dimension | Current State | Honest Grade |
|---|---|---|
| **User capacity** | Single VPS handles 50,000+ MAU comfortably | A — architecture is not the constraint |
| **Realistic near-term users** | 500–2,000 MAU by Month 9 if pilot succeeds | Dependent on G3 and distribution, not architecture |
| **Transport security** | HTTPS specified; webhook signature not yet coded | C — must be implemented before any real users |
| **Application security** | Rate limiting and idempotency specified, not coded | C — must ship on first feature branch |
| **Data security** | Encryption specified, not yet configured | C — must be done when models are written |
| **Supply chain security** | Locked deps, Dependabot, pinned Actions | A |
| **Architecture simplicity** | Single-node, stateless app, correct for scale | A |
| **Failure recovery** | Backup specified but not tested, no runbook | D — fixable before launch |
| **Platform risk (Meta)** | No mitigation possible | F — accepted, not solvable |
| **Operational observability** | No monitoring yet | D — UptimeRobot takes 10 minutes to set up |
| **Foundation for future scale** | Stateless app, DB schema clean, migrations in place | B+ — solid once the runbook and monitoring gaps are closed |

The foundation is the right foundation. The gaps are operational and implementation gaps, not design flaws. Every C and D grade above is closable with a single focused PR or afternoon of configuration work. None of them require rethinking the architecture.
