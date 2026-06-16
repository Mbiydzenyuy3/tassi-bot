from fastapi import FastAPI

from tassi.config import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """
    Application factory. Accepts an optional Settings instance so tests can
    inject configuration without touching environment variables.
    """
    cfg = settings or Settings()

    app = FastAPI(
        title="Tassi",
        description="WhatsApp tax-compliance assistant for Cameroonian RSI SMEs.",
        version="0.1.0",
        # Disable API docs in production — only expose in debug/dev mode
        docs_url="/docs" if cfg.debug else None,
        redoc_url="/redoc" if cfg.debug else None,
    )

    @app.get("/health", tags=["ops"], summary="Liveness probe")
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": "tassi"}

    return app


# Module-level app used by uvicorn: uvicorn tassi.main:app
app = create_app()
