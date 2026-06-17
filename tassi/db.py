"""Database engine, session factory, and declarative base for Tassi."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Shared declarative base imported by all Tassi models."""


def build_engine(database_url: str) -> AsyncEngine:
    """
    Create an async SQLAlchemy engine from a connection URL.
    Called once at app startup — never at module import time.
    pool_pre_ping=True recycles stale connections silently.
    """
    return create_async_engine(database_url, pool_pre_ping=True)


def build_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """
    Create a session factory bound to the given engine.
    expire_on_commit=False keeps model attributes accessible after commit
    without requiring a new SELECT — important for async code where lazy
    loading is not available.
    """
    return async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    """
    Yield one AsyncSession per request.
    Commits on clean exit, rolls back on any exception, always closes.
    Intended to be used as a FastAPI dependency via Depends().
    """
    session: AsyncSession = session_factory()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
