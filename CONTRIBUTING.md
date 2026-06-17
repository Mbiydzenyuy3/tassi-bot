# Contributing to Tassi

## Guiding Principles

This project follows the [Karpathy Guidelines](`.claude/andrej-karpathy-skills-main/CLAUDE.md`):

1. **Think Before Coding** — state assumptions explicitly, surface trade-offs, ask before guessing
2. **Simplicity First** — minimum code that satisfies the requirement; nothing speculative
3. **Surgical Changes** — touch only what you must; don't refactor adjacent code
4. **Goal-Driven Execution** — write the test first, then make it pass

When in doubt: would a senior engineer say this is overcomplicated? If yes, simplify.

---

## Branch Strategy

```
main          — production-ready, protected; direct commits blocked
  └── development  — integration branch; PRs merge here first
        └── feat/short-description   — feature work
        └── fix/short-description    — bug fixes
        └── chore/short-description  — tooling, deps, config
```

**Rule:** never commit directly to `main` or `development`. Open a PR.

---

## Development Setup

### Install dependencies

```bash
# Prerequisites: Python 3.12, uv (https://docs.astral.sh/uv/), Docker
git clone git@github.com:Mbiydzenyuy3/tassi-bot.git
cd tassi-bot
cp .env.example .env   # fill in real values

# Install all dependencies (app + dev + test groups) and pre-commit hooks
make setup
# Equivalent to: uv sync --all-groups && pre-commit install --hook-type pre-commit --hook-type commit-msg

# Install only dev/test dependencies without running hook setup:
# uv sync --group dev
```

### Run the app

Start the backing services and the app:

```bash
# Start Postgres + Redis in the background
docker compose up postgres redis -d

# Apply pending migrations (first run, and after any new migration file)
make migrate

# Run the app with hot-reload
make dev
# Equivalent to: uv run uvicorn tassi.main:app --reload --port 8000
```

Or run the full stack (app + DB + Redis) together in containers:

```bash
make docker-up         # all services in background
make docker-logs       # follow app container logs
```

Health check: `curl http://localhost:8000/health`

---

## Commit Messages (Conventional Commits)

All commits must follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<optional scope>): <short summary>

[optional body]
[optional footer: BREAKING CHANGE: ...]
```

**Types:**

| Type | When to use |
|---|---|
| `feat` | New feature (triggers minor version bump) |
| `fix` | Bug fix (triggers patch bump) |
| `docs` | Documentation only |
| `chore` | Tooling, config, CI — no production code change |
| `refactor` | Code restructure with no behavior change |
| `test` | Adding or fixing tests |
| `perf` | Performance improvement |

**Examples:**

```
feat(tax): add RSI acompte calculation endpoint

fix(payment): handle Campay webhook delivery failure with STATUS command

docs(srs): add Gate G1 resolution — CAC is additive per Art. 581 CGI
```

The `commitizen` hook enforces this format on every commit. If it rejects your message, run `git commit` again with the corrected format, or use `uv run cz commit` for an interactive prompt.

---

## Code Quality

All checks must pass before a PR can merge:

```bash
make check     # ruff lint + black format-check + mypy type-check
make test      # pytest with ≥99.98% branch coverage
```

**Never** bypass the coverage gate. If a new line can't realistically be tested, it almost certainly shouldn't be there — but if it genuinely can't be avoided, annotate it with `# pragma: no cover` and explain why in the PR description.

**Financial math:** always use `decimal.Decimal`, never `float`. A test that catches a rounding error is required alongside any calculation change.

---

## Validation Gates

Before building features that touch tax math, payments, or subscriptions, check SRS §3:

| Gate | Status | Blocks |
|---|---|---|
| G1 — CAC additive or included? | **OPEN** | `CAC_MODE=ADDITIVE\|INCLUDED` in config, showing combined total |
| G2 — Fiscal advisory license needed? | **OPEN** | Guarantee-style marketing language in bot messages |
| G3 — Users will pay for Plus at what price? | **OPEN** | Real `PLUS_PRICE_XAF`, enabling `FEATURE_PLUS_REMINDERS` |

Do not write code that assumes a gate is closed until it is explicitly closed and the relevant SRS section is updated.

---

## Filing Window Code Freeze

**No deployments between the 8th and 16th of each calendar month** (SRS NFR-AVAIL-2). This is the peak filing window. Code changes on `development` are fine; merges to `main` and deployments are blocked.

---

## Pull Request Checklist

Use the PR template (`.github/pull_request_template.md`). Key items:

- All CI jobs green
- Coverage ≥ 99.98% (CI enforces this)
- `.env.example` updated for any new config variables
- `docs/` updated if a requirement or design decision changed
- No deploy during the 8th–16th filing window
