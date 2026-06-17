from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from tassi.config import Settings
from tassi.db import build_engine, build_session_factory


def create_app(settings: Settings | None = None) -> FastAPI:
    """
    Application factory. Accepts an optional Settings instance so tests can
    inject configuration without touching environment variables.
    """
    cfg = settings or Settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        engine = build_engine(cfg.database_url)
        app.state.engine = engine
        app.state.db_factory = build_session_factory(engine)
        yield
        await engine.dispose()

    app = FastAPI(
        title="Tassi",
        description="WhatsApp tax-compliance assistant for Cameroonian RSI SMEs.",
        version="0.1.0",
        docs_url="/docs" if cfg.debug else None,
        redoc_url="/redoc" if cfg.debug else None,
        lifespan=lifespan,
    )

    @app.get("/health", tags=["ops"], summary="Liveness probe")
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": "tassi"}

    return app


# Module-level app used by uvicorn: uvicorn tassi.main:app
app = create_app()
