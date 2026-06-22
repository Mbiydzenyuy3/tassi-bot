"""Tests for tassi/reminders.py — T11, T12, T13 + idempotency + error handling."""

import uuid
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from tassi.config import Settings
from tassi.reminders import (
    make_daily_reminder_job,
    send_day_10_reminders,
    send_day_14_reminders,
    send_renewal_prompts,
)

# ── Fixtures ──────────────────────────────────────────────────────────────────

_BASE_SETTINGS = {
    "database_url": "postgresql+psycopg://x:x@localhost/x",
    "redis_url": "redis://localhost",
    "meta_verify_token": "t",
    "meta_app_secret": "s",
    "meta_phone_number_id": "phone-id",
    "meta_access_token": "token",
    "campay_username": "u",
    "campay_password": "p",
    "campay_application_token": "tok",
    "environment": "test",
}


def _cfg(**overrides: object) -> Settings:
    return Settings(**{**_BASE_SETTINGS, **overrides})  # type: ignore[arg-type]


def _make_user(whatsapp_id: str = "+237600000001") -> MagicMock:
    """Fake User ORM object."""
    u = MagicMock()
    u.id = uuid.uuid4()
    u.whatsapp_id = whatsapp_id
    return u


def _make_subscription(user_id: uuid.UUID | None = None, days_until_expiry: int = 2) -> MagicMock:
    """Fake Subscription ORM object expiring in `days_until_expiry` days."""
    s = MagicMock()
    s.id = uuid.uuid4()
    s.user_id = user_id or uuid.uuid4()
    s.status = "ACTIVE"
    s.period_end = datetime.now(tz=UTC) + timedelta(days=days_until_expiry)
    return s


def _make_db(rows: list | None = None) -> AsyncMock:
    """Mock AsyncSession whose execute() returns `rows` as scalars."""
    db = AsyncMock()
    result = MagicMock()
    result.scalars.return_value.all.return_value = rows or []
    result.all.return_value = rows or []
    db.execute.return_value = result
    db.add = MagicMock()
    db.commit = AsyncMock()
    return db


# ── T11: day_14 reminder sent to filers ──────────────────────────────────────


class TestSendDay14Reminders:
    async def test_T11_day_14_reminder_sent_to_filers(self) -> None:
        user = _make_user()
        db = _make_db([user])
        cfg = _cfg()

        with patch("tassi.reminders.send_text_message", new_callable=AsyncMock) as mock_send:
            count = await send_day_14_reminders("2026-06", db, cfg)

        assert count == 1
        mock_send.assert_awaited_once()
        call_kwargs = mock_send.call_args
        # Message sent to correct recipient
        assert user.whatsapp_id in call_kwargs.args or user.whatsapp_id in str(call_kwargs)

    async def test_day_14_reminder_idempotent(self) -> None:
        """Called twice on the same period — sends once total."""
        user = _make_user()
        # First call: db returns the user (not yet reminded)
        # Second call: db returns [] (already reminded — idempotency in query)
        db = _make_db([user])
        db_empty = _make_db([])
        cfg = _cfg()

        with patch("tassi.reminders.send_text_message", new_callable=AsyncMock) as mock_send:
            first = await send_day_14_reminders("2026-06", db, cfg)
            second = await send_day_14_reminders("2026-06", db_empty, cfg)

        assert first == 1
        assert second == 0
        assert mock_send.await_count == 1

    async def test_day_14_no_filers_sends_nothing(self) -> None:
        db = _make_db([])
        cfg = _cfg()

        with patch("tassi.reminders.send_text_message", new_callable=AsyncMock) as mock_send:
            count = await send_day_14_reminders("2026-06", db, cfg)

        assert count == 0
        mock_send.assert_not_awaited()


# ── T12: day_10 flag off → no sends ──────────────────────────────────────────


class TestSendDay10Reminders:
    async def test_T12_day_10_reminder_not_sent_when_flag_off(self) -> None:
        db = _make_db([_make_user()])
        cfg = _cfg(feature_plus_reminders=False)

        with patch("tassi.reminders.send_text_message", new_callable=AsyncMock) as mock_send:
            count = await send_day_10_reminders("2026-06", db, cfg)

        assert count == 0
        mock_send.assert_not_awaited()

    async def test_day_10_reminder_sent_when_flag_on(self) -> None:
        user = _make_user()
        db = _make_db([user])
        cfg = _cfg(feature_plus_reminders=True)

        with patch("tassi.reminders.send_text_message", new_callable=AsyncMock) as mock_send:
            count = await send_day_10_reminders("2026-06", db, cfg)

        assert count == 1
        mock_send.assert_awaited_once()

    async def test_day_10_flag_on_no_plus_users_does_not_commit(self) -> None:
        """Flag is on but no Plus users remain to remind — covers if users: false branch."""
        db = _make_db([])
        cfg = _cfg(feature_plus_reminders=True)

        with patch("tassi.reminders.send_text_message", new_callable=AsyncMock) as mock_send:
            count = await send_day_10_reminders("2026-06", db, cfg)

        assert count == 0
        mock_send.assert_not_awaited()
        db.commit.assert_not_awaited()


# ── T13: renewal prompt sent 3 days before expiry ────────────────────────────


class TestSendRenewalPrompts:
    async def test_T13_renewal_prompt_sent_3_days_before_expiry(self) -> None:
        user = _make_user()
        sub = _make_subscription(user_id=user.id, days_until_expiry=2)
        # execute() returns [(sub, user)] pairs
        db = AsyncMock()
        result = MagicMock()
        result.all.return_value = [(sub, user)]
        db.execute.return_value = result
        db.add = MagicMock()
        db.commit = AsyncMock()
        cfg = _cfg()

        with patch("tassi.reminders.send_text_message", new_callable=AsyncMock) as mock_send:
            count = await send_renewal_prompts(db, cfg)

        assert count == 1
        mock_send.assert_awaited_once()

    async def test_renewal_no_expiring_subs_sends_nothing(self) -> None:
        db = AsyncMock()
        result = MagicMock()
        result.all.return_value = []
        db.execute.return_value = result
        db.add = MagicMock()
        db.commit = AsyncMock()
        cfg = _cfg()

        with patch("tassi.reminders.send_text_message", new_callable=AsyncMock) as mock_send:
            count = await send_renewal_prompts(db, cfg)

        assert count == 0
        mock_send.assert_not_awaited()


# ── Daily job error handling ──────────────────────────────────────────────────


class TestDailyReminderJob:
    async def test_daily_job_does_not_crash_on_error(self) -> None:
        """Meta API raises — job catches and logs, does not re-raise."""
        db = _make_db([_make_user()])

        async def _boom(*args: object, **kwargs: object) -> None:
            raise RuntimeError("meta api is down")

        async def _db_factory_cm() -> AsyncMock:
            return db

        # Context manager factory: `async with db_factory() as db`
        class _FakeFactory:
            def __call__(self) -> "_FakeFactory":
                return self

            async def __aenter__(self) -> AsyncMock:
                return db

            async def __aexit__(self, *args: object) -> None:
                pass

        job = make_daily_reminder_job(_FakeFactory(), _cfg())

        with patch("tassi.reminders.send_text_message", new=_boom):
            # Must not raise — error is caught and logged
            await job()

    async def test_daily_job_calls_renewal_prompts_every_day(self) -> None:
        """send_renewal_prompts is always called, regardless of day of month."""

        class _FakeFactory:
            def __call__(self) -> "_FakeFactory":
                return self

            async def __aenter__(self) -> AsyncMock:
                return _make_db([])

            async def __aexit__(self, *args: object) -> None:
                pass

        job = make_daily_reminder_job(_FakeFactory(), _cfg())

        with (
            patch("tassi.reminders.send_renewal_prompts", new_callable=AsyncMock) as mock_renewal,
            patch("tassi.reminders.send_day_14_reminders", new_callable=AsyncMock),
            patch("tassi.reminders.send_day_10_reminders", new_callable=AsyncMock),
        ):
            await job()

        mock_renewal.assert_awaited_once()

    async def test_daily_job_sends_day14_on_day_14(self) -> None:
        """When today is the 14th, send_day_14_reminders is called — covers line 192."""

        class _FakeFactory:
            def __call__(self) -> "_FakeFactory":
                return self

            async def __aenter__(self) -> AsyncMock:
                return _make_db([])

            async def __aexit__(self, *args: object) -> None:
                pass

        job = make_daily_reminder_job(_FakeFactory(), _cfg())
        fake_now = datetime(2026, 6, 14, 3, 0, tzinfo=UTC)

        with (
            patch("tassi.reminders.datetime") as mock_dt,
            patch("tassi.reminders.send_day_14_reminders", new_callable=AsyncMock) as mock_14,
            patch("tassi.reminders.send_day_10_reminders", new_callable=AsyncMock),
            patch("tassi.reminders.send_renewal_prompts", new_callable=AsyncMock),
        ):
            mock_dt.now.return_value = fake_now
            await job()

        mock_14.assert_awaited_once()

    async def test_daily_job_sends_day10_on_day_10(self) -> None:
        """When today is the 10th, send_day_10_reminders is called — covers line 194."""

        class _FakeFactory:
            def __call__(self) -> "_FakeFactory":
                return self

            async def __aenter__(self) -> AsyncMock:
                return _make_db([])

            async def __aexit__(self, *args: object) -> None:
                pass

        job = make_daily_reminder_job(_FakeFactory(), _cfg())
        fake_now = datetime(2026, 6, 10, 3, 0, tzinfo=UTC)

        with (
            patch("tassi.reminders.datetime") as mock_dt,
            patch("tassi.reminders.send_day_10_reminders", new_callable=AsyncMock) as mock_10,
            patch("tassi.reminders.send_day_14_reminders", new_callable=AsyncMock),
            patch("tassi.reminders.send_renewal_prompts", new_callable=AsyncMock),
        ):
            mock_dt.now.return_value = fake_now
            await job()

        mock_10.assert_awaited_once()
