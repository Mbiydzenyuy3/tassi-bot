"""Tests for tassi/db.py — engine factory, session factory, session lifecycle."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from tassi.db import Base, build_engine, build_session_factory, get_db_session

# Use a URL that is syntactically valid but will never be connected to in these tests.
_TEST_DB_URL = "postgresql+psycopg://tassi:tassi@localhost:5432/tassi_test"


class TestBase:
    def test_has_metadata(self) -> None:
        assert hasattr(Base, "metadata")

    def test_has_registry(self) -> None:
        assert hasattr(Base, "registry")


class TestBuildEngine:
    def test_returns_async_engine(self) -> None:
        engine = build_engine(_TEST_DB_URL)
        assert isinstance(engine, AsyncEngine)

    def test_url_is_preserved(self) -> None:
        engine = build_engine(_TEST_DB_URL)
        assert "tassi_test" in str(engine.url)

    def test_different_urls_produce_different_engines(self) -> None:
        url_a = "postgresql+psycopg://a:a@localhost/db_a"
        url_b = "postgresql+psycopg://b:b@localhost/db_b"
        engine_a = build_engine(url_a)
        engine_b = build_engine(url_b)
        assert str(engine_a.url) != str(engine_b.url)


class TestBuildSessionFactory:
    def test_returns_async_sessionmaker(self) -> None:
        engine = build_engine(_TEST_DB_URL)
        factory = build_session_factory(engine)
        assert isinstance(factory, async_sessionmaker)

    def test_expire_on_commit_is_false(self) -> None:
        # expire_on_commit=False is required in async code — lazy loading
        # is not available, so attributes must remain accessible post-commit.
        engine = build_engine(_TEST_DB_URL)
        factory = build_session_factory(engine)
        assert factory.kw.get("expire_on_commit") is False


class TestGetDbSession:
    async def test_yields_exactly_one_session(self) -> None:
        mock_session = AsyncMock(spec=AsyncSession)
        mock_factory = MagicMock(return_value=mock_session)

        yielded: list[AsyncSession] = []
        async for session in get_db_session(mock_factory):
            yielded.append(session)

        assert len(yielded) == 1
        assert yielded[0] is mock_session

    async def test_yields_the_session_from_factory(self) -> None:
        mock_session = AsyncMock(spec=AsyncSession)
        mock_factory = MagicMock(return_value=mock_session)

        async for session in get_db_session(mock_factory):
            assert session is mock_session

    async def test_commits_on_clean_exit(self) -> None:
        mock_session = AsyncMock(spec=AsyncSession)
        mock_factory = MagicMock(return_value=mock_session)

        async for _ in get_db_session(mock_factory):
            pass  # clean exit — no exception

        mock_session.commit.assert_awaited_once()
        mock_session.rollback.assert_not_awaited()

    async def test_closes_on_clean_exit(self) -> None:
        mock_session = AsyncMock(spec=AsyncSession)
        mock_factory = MagicMock(return_value=mock_session)

        async for _ in get_db_session(mock_factory):
            pass

        mock_session.close.assert_awaited_once()

    async def test_rolls_back_on_exception(self) -> None:
        # FastAPI throws exceptions into generator dependencies via athrow() —
        # that is what we replicate here to exercise the except block.
        mock_session = AsyncMock(spec=AsyncSession)
        mock_factory = MagicMock(return_value=mock_session)

        gen = get_db_session(mock_factory)
        await gen.__anext__()  # advance to the yield

        with pytest.raises(ValueError, match="test error"):
            await gen.athrow(ValueError("test error"))

        mock_session.rollback.assert_awaited_once()
        mock_session.commit.assert_not_awaited()

    async def test_closes_on_exception(self) -> None:
        # finally block must execute even when an exception propagates
        mock_session = AsyncMock(spec=AsyncSession)
        mock_factory = MagicMock(return_value=mock_session)

        gen = get_db_session(mock_factory)
        await gen.__anext__()

        with pytest.raises(RuntimeError):
            await gen.athrow(RuntimeError("boom"))

        mock_session.close.assert_awaited_once()

    async def test_exception_is_reraised(self) -> None:
        # rollback must not swallow the original exception
        mock_session = AsyncMock(spec=AsyncSession)
        mock_factory = MagicMock(return_value=mock_session)

        gen = get_db_session(mock_factory)
        await gen.__anext__()

        with pytest.raises(ZeroDivisionError):
            await gen.athrow(ZeroDivisionError("on purpose"))
