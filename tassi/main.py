from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Query, Request, Response
from redis.asyncio import ConnectionPool, Redis
from sqlalchemy.ext.asyncio import AsyncSession

from tassi.chat import handle_message
from tassi.config import Settings
from tassi.db import build_engine, build_session_factory
from tassi.deps import get_cfg, get_db, get_redis
from tassi.payments import process_payment_callback
from tassi.reminders import make_daily_reminder_job
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
        scheduler = AsyncIOScheduler()
        scheduler.add_job(
            make_daily_reminder_job(app.state.db_factory, cfg),
            "cron",
            hour=3,
            minute=0,
        )
        scheduler.start()
        yield
        scheduler.shutdown()
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
                    msisdn = str(message.get("from", ""))
                    message_id = str(message.get("id", ""))
                    message_text = str(
                        message.get("text", {}).get("body", "")
                        if isinstance(message.get("text"), dict)
                        else message.get("text", "")
                    )

                    if not message_text:
                        continue  # skip non-text messages (images, voice notes, stickers)

                    if await is_rate_limited(redis, msisdn, cfg.rate_limit_per_60s):
                        continue

                    if await is_duplicate_message(redis, message_id):
                        continue

                    background_tasks.add_task(
                        handle_message,
                        msisdn,
                        message_text,
                        message_id,
                        request.app.state.db_factory,
                        redis,
                        cfg,
                    )

        return {"status": "ok"}

    @app.post("/campay/webhook", tags=["payments"], status_code=200)
    async def campay_callback(
        request: Request,
        background_tasks: BackgroundTasks,
        cfg: Settings = Depends(get_cfg),
        db: AsyncSession = Depends(get_db),
    ) -> dict[str, str]:
        """
        Receive Campay payment status callback (FR-PAY-3).
        Verifies app_token in the payload before processing.
        """
        try:
            payload = await request.json()
        except Exception as exc:
            raise HTTPException(status_code=400, detail="invalid json") from exc

        if payload.get("app_token") != cfg.campay_application_token:
            raise HTTPException(status_code=403, detail="invalid app_token")

        campay_reference = str(payload.get("reference", ""))
        raw_status = str(payload.get("status", "")).upper()
        status = "SUCCESS" if raw_status == "SUCCESSFUL" else raw_status

        if not campay_reference:
            raise HTTPException(status_code=400, detail="missing reference")

        background_tasks.add_task(
            process_payment_callback,
            campay_reference,
            status,
            db,
            cfg,
        )
        return {"status": "ok"}

    return app


# Module-level app used by uvicorn: uvicorn tassi.main:app
app = create_app()
