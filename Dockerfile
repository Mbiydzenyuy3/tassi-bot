# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

# Install uv (fast dependency resolver/installer)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency manifests first so Docker layer cache is reused when only
# source code changes (not dependencies).
COPY pyproject.toml uv.lock ./

# Install production dependencies into an isolated venv; never install dev deps
# or the project itself (we copy source in the runtime stage instead).
RUN uv sync --no-dev --frozen --no-install-project

# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

WORKDIR /app

# Security: run as a non-root user
RUN addgroup --system tassi && adduser --system --ingroup tassi tassi

# Copy the pre-built venv from builder (no compiler/build tools in runtime)
COPY --from=builder --chown=tassi:tassi /app/.venv /app/.venv

# Copy application source
COPY --chown=tassi:tassi tassi/ tassi/

USER tassi

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app"

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "tassi.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
