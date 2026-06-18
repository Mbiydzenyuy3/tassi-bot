from collections.abc import AsyncGenerator
from typing import cast

from fastapi import Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from tassi.config import Settings


def get_cfg(request: Request) -> Settings:
    """Return the Settings instance stored on app.state (set at startup)."""
    return cast(Settings, request.app.state.cfg)


async def get_redis(request: Request) -> AsyncGenerator[Redis, None]:  # type: ignore[type-arg]
    """Yield the Redis client from the connection pool stored on app.state."""
    yield cast(Redis, request.app.state.redis)  # type: ignore[type-arg]


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """Yield an async DB session from the factory stored on app.state."""
    async with request.app.state.db_factory() as session:
        yield session
