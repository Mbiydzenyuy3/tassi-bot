"""Tests for tassi.deps — FastAPI dependency functions."""

from unittest.mock import AsyncMock, MagicMock

from redis.asyncio import Redis

from tassi.config import Settings
from tassi.deps import get_cfg, get_db, get_redis


def _mock_request(**state_attrs: object) -> MagicMock:
    req = MagicMock()
    for key, val in state_attrs.items():
        setattr(req.app.state, key, val)
    return req


class TestGetCfg:
    def test_returns_settings_from_app_state(self) -> None:
        cfg = Settings(environment="test")
        req = _mock_request(cfg=cfg)
        assert get_cfg(req) is cfg


class TestGetRedis:
    async def test_yields_redis_from_app_state(self) -> None:
        redis = MagicMock(spec=Redis)
        req = _mock_request(redis=redis)
        async for client in get_redis(req):
            assert client is redis


class TestGetDb:
    async def test_yields_session_from_db_factory(self) -> None:
        mock_session = AsyncMock()
        mock_factory = MagicMock()
        mock_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        mock_factory.return_value.__aexit__ = AsyncMock(return_value=False)
        req = _mock_request(db_factory=mock_factory)
        async for session in get_db(req):
            assert session is mock_session
