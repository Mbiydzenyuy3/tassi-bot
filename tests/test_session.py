"""
Tests for tassi.session — Redis session, dedup, rate limiting.
Uses a real Redis at redis://localhost:6379/1 (test DB index 1).
Each test flushes the test DB for isolation.
"""

import asyncio
from unittest.mock import AsyncMock

import pytest_asyncio
from redis.asyncio import Redis
from redis.exceptions import RedisError

from tassi.session import (
    clear_session,
    get_session,
    is_duplicate_message,
    is_rate_limited,
    set_session,
)

_REDIS_URL = "redis://localhost:6379/1"


@pytest_asyncio.fixture
async def redis() -> Redis:
    client = Redis.from_url(_REDIS_URL, decode_responses=True)
    await client.flushdb()
    yield client
    await client.flushdb()
    await client.aclose()


class TestGetSetClearSession:
    async def test_get_session_missing_returns_empty(self, redis: Redis) -> None:
        assert await get_session(redis, "2370000000000") == {}

    async def test_set_and_get_session_roundtrip(self, redis: Redis) -> None:
        state = {"step": "ask_revenue", "lang": "fr"}
        await set_session(redis, "2370000000000", state)
        assert await get_session(redis, "2370000000000") == state

    async def test_clear_session_removes_key(self, redis: Redis) -> None:
        await set_session(redis, "2370000000000", {"step": "done"})
        await clear_session(redis, "2370000000000")
        assert await get_session(redis, "2370000000000") == {}

    async def test_session_expires_after_ttl(self, redis: Redis) -> None:
        import tassi.session as s_mod

        original_ttl = s_mod._SESSION_TTL
        s_mod._SESSION_TTL = 1
        try:
            await set_session(redis, "2370000000001", {"step": "temp"})
            await asyncio.sleep(1.5)
            assert await get_session(redis, "2370000000001") == {}
        finally:
            s_mod._SESSION_TTL = original_ttl


class TestSessionDegradedMode:
    """Verify all session functions handle RedisError gracefully (NFR-AVAIL-3)."""

    async def test_get_session_redis_error_returns_empty(self, redis: Redis) -> None:
        redis.get = AsyncMock(side_effect=RedisError("down"))
        assert await get_session(redis, "msisdn") == {}

    async def test_set_session_redis_error_is_noop(self, redis: Redis) -> None:
        redis.set = AsyncMock(side_effect=RedisError("down"))
        await set_session(redis, "msisdn", {"step": "x"})  # must not raise

    async def test_clear_session_redis_error_is_noop(self, redis: Redis) -> None:
        redis.delete = AsyncMock(side_effect=RedisError("down"))
        await clear_session(redis, "msisdn")  # must not raise

    async def test_is_duplicate_redis_error_returns_false(self, redis: Redis) -> None:
        redis.setnx = AsyncMock(side_effect=RedisError("down"))
        assert await is_duplicate_message(redis, "msg-id") is False

    async def test_is_rate_limited_redis_error_returns_false(self, redis: Redis) -> None:
        redis.incr = AsyncMock(side_effect=RedisError("down"))
        assert await is_rate_limited(redis, "msisdn", 10) is False


class TestIsDuplicateMessage:
    async def test_first_call_returns_false(self, redis: Redis) -> None:
        assert await is_duplicate_message(redis, "msg-abc-001") is False

    async def test_second_call_same_id_returns_true(self, redis: Redis) -> None:
        await is_duplicate_message(redis, "msg-abc-002")
        assert await is_duplicate_message(redis, "msg-abc-002") is True

    async def test_different_ids_are_independent(self, redis: Redis) -> None:
        assert await is_duplicate_message(redis, "msg-x-001") is False
        assert await is_duplicate_message(redis, "msg-x-002") is False


class TestIsRateLimited:
    async def test_first_calls_not_limited(self, redis: Redis) -> None:
        limit = 3
        for _ in range(limit):
            assert await is_rate_limited(redis, "237600000001", limit) is False

    async def test_call_beyond_limit_is_limited(self, redis: Redis) -> None:
        limit = 3
        for _ in range(limit):
            await is_rate_limited(redis, "237600000002", limit)
        assert await is_rate_limited(redis, "237600000002", limit) is True

    async def test_different_msisdns_are_independent(self, redis: Redis) -> None:
        limit = 1
        await is_rate_limited(redis, "237600000003", limit)
        assert await is_rate_limited(redis, "237600000003", limit) is True
        assert await is_rate_limited(redis, "237600000004", limit) is False
