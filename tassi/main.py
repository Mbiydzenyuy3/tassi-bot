from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Query, Request, Response
from redis.asyncio import ConnectionPool, Redis

from tassi.chat import handle_message
from tassi.config import Settings
from tassi.db import build_engine, build_session_factory
from tassi.deps import get_cfg, get_redis
from tassi.security import verify_meta_signature
from tassi.session import is_duplicate_message, is_rate_limited


def create_app(settings: Settings | None = None) -> FastAPI:
    """
    Application factory. Accepts an optional Settings instance so tests can
    inject configuration without touching environment variables.
    """
    cfg = settings or Settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        engine = build_engine(cfg.database_url)
        pool: ConnectionPool = ConnectionPool.from_url(cfg.redis_url, decode_responses=True)  # type: ignore[type-arg]
        app.state.cfg = cfg
        app.state.engine = engine
        app.state.db_factory = build_session_factory(engine)
        app.state.redis = Redis(connection_pool=pool)
        yield
        await app.state.redis.aclose()
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

    @app.get("/webhook", tags=["webhook"], summary="Meta webhook verification handshake")
    async def verify_webhook(
        hub_mode: str = Query(alias="hub.mode"),
        hub_verify_token: str = Query(alias="hub.verify_token"),
        hub_challenge: str = Query(alias="hub.challenge"),
        cfg: Settings = Depends(get_cfg),
    ) -> Response:
        """Return hub_challenge as plain text when token matches (FR-CHAT-1)."""
        if hub_mode == "subscribe" and hub_verify_token == cfg.meta_verify_token:
            return Response(content=hub_challenge, media_type="text/plain")
        raise HTTPException(status_code=403, detail="forbidden")

    @app.post("/webhook", tags=["webhook"], status_code=200)
    async def receive_webhook(
        request: Request,
        background_tasks: BackgroundTasks,
        cfg: Settings = Depends(get_cfg),
        redis: Redis = Depends(get_redis),  # type: ignore[type-arg]
    ) -> dict[str, str]:
        """
        Ingest a WhatsApp message. Acks immediately (NFR-PERF-1) and
        dispatches processing to a background task (FR-CHAT-1, FR-CHAT-6).
        """
        body = await request.body()

        sig = request.headers.get("X-Hub-Signature-256", "")
        if not verify_meta_signature(body, sig, cfg.meta_app_secret):
            raise HTTPException(status_code=403, detail="invalid signature")

        try:
            payload = await request.json()
        except Exception as exc:
            raise HTTPException(status_code=400, detail="invalid json") from exc

        for entry in payload.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                for message in value.get("messages", []):
                    msisdn = message.get("from", "")
                    message_id = message.get("id", "")

                    if await is_rate_limited(redis, msisdn, cfg.rate_limit_per_60s):
                        continue

                    if await is_duplicate_message(redis, message_id):
                        continue

                    background_tasks.add_task(handle_message, message, cfg)

        return {"status": "ok"}

    return app


# Module-level app used by uvicorn: uvicorn tassi.main:app
app = create_app()
