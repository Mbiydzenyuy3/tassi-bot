import json
import logging

from redis.asyncio import Redis
from redis.exceptions import RedisError

_log = logging.getLogger(__name__)

_SESSION_TTL = 7200  # 2 hours — FR-CHAT-2
_DEDUP_TTL = 86400  # 24 hours — long enough to cover any Meta retry window
_RATE_TTL = 60  # 60-second window — FR-DATA-3


async def get_session(redis: Redis, msisdn: str) -> dict[str, object]:  # type: ignore[type-arg]
    """Return current conversation state. Returns {} if absent or Redis is down."""
    try:
        raw = await redis.get(f"session:{msisdn}")
        return json.loads(raw) if raw else {}
    except RedisError:
        _log.warning("redis unavailable — get_session returning empty state")
        return {}


async def set_session(redis: Redis, msisdn: str, state: dict[str, object]) -> None:  # type: ignore[type-arg]
    """Persist conversation state with a 2-hour TTL. No-op if Redis is down."""
    try:
        await redis.set(f"session:{msisdn}", json.dumps(state), ex=_SESSION_TTL)
    except RedisError:
        _log.warning("redis unavailable — set_session skipped")


async def clear_session(redis: Redis, msisdn: str) -> None:  # type: ignore[type-arg]
    """Delete session key. No-op if Redis is down."""
    try:
        await redis.delete(f"session:{msisdn}")
    except RedisError:
        _log.warning("redis unavailable — clear_session skipped")


async def is_duplicate_message(redis: Redis, message_id: str) -> bool:  # type: ignore[type-arg]
    """
    SETNX on seen_msg:<message_id> with 24h TTL.
    Returns True if this message_id was already seen (FR-CHAT-6).
    Returns False (process the message) if Redis is down — acceptable degradation.
    """
    try:
        inserted = await redis.setnx(f"seen_msg:{message_id}", "1")
        if inserted:
            await redis.expire(f"seen_msg:{message_id}", _DEDUP_TTL)
        return not inserted
    except RedisError:
        _log.warning("redis unavailable — treating message as new (possible duplicate)")
        return False


async def is_rate_limited(redis: Redis, msisdn: str, limit: int) -> bool:  # type: ignore[type-arg]
    """
    Increment rate_limit:<msisdn> within a 60s window.
    Returns True if the count exceeds `limit` (FR-DATA-3).
    Returns False if Redis is down — acceptable degradation.
    """
    key = f"rate_limit:{msisdn}"
    try:
        count = await redis.incr(key)
        if count == 1:
            await redis.expire(key, _RATE_TTL)
        return count > limit
    except RedisError:
        _log.warning("redis unavailable — rate limiting disabled")
        return False
