"""
Tests for tassi.payments.process_payment_callback (FR-PAY-3).
All DB and HTTP calls are mocked — no Postgres or Meta API needed.
"""

import uuid
from unittest.mock import AsyncMock, MagicMock, patch

from tassi.config import Settings
from tassi.payments import process_payment_callback

_CFG = Settings(
    meta_phone_number_id="test-phone-id",
    meta_access_token="test-access-token",
    campay_username="u",
    campay_password="p",
    campay_application_token="test-token",
)
_MSISDN = "237600000001"
_REF = "CPY-CALLBACK-001"


def _mock_tx(status: str = "PENDING") -> MagicMock:
    tx = MagicMock()
    tx.campay_reference = _REF
    tx.status = status
    tx.user_id = uuid.uuid4()
    tx.amount_xaf = 500
    tx.updated_at = None
    tx.subscription_id = None
    return tx


def _mock_user(language: str = "fr") -> MagicMock:
    user = MagicMock()
    user.whatsapp_id = _MSISDN
    user.language = language
    return user


def _make_db(tx: MagicMock | None, user: MagicMock | None = None) -> AsyncMock:
    session = AsyncMock()

    tx_result = MagicMock()
    tx_result.scalar_one_or_none.return_value = tx

    user_result = MagicMock()
    if user is not None:
        user_result.scalar_one.return_value = user

    session.execute = AsyncMock(side_effect=[tx_result, user_result])
    session.add = MagicMock()
    session.flush = AsyncMock()

    begin_ctx = AsyncMock()
    begin_ctx.__aenter__ = AsyncMock(return_value=None)
    begin_ctx.__aexit__ = AsyncMock(return_value=False)
    session.begin = MagicMock(return_value=begin_ctx)

    return session


class TestProcessPaymentCallback:
    async def test_success_updates_tx_and_creates_subscription(self) -> None:
        tx = _mock_tx()
        user = _mock_user()
        db = _make_db(tx, user)

        with patch("tassi.payments.send_text_message", new_callable=AsyncMock) as mock_send:
            await process_payment_callback(_REF, "SUCCESS", db, _CFG)

        assert tx.status == "SUCCESS"
        assert tx.updated_at is not None
        db.add.assert_called_once()
        db.flush.assert_called_once()
        mock_send.assert_called_once()
        call_args = mock_send.call_args[0]
        assert call_args[2] == _MSISDN
        assert "Tassi Plus" in call_args[3] or "confirmé" in call_args[3]

    async def test_failed_updates_status_only(self) -> None:
        tx = _mock_tx()
        user = _mock_user()
        db = _make_db(tx, user)

        with patch("tassi.payments.send_text_message", new_callable=AsyncMock) as mock_send:
            await process_payment_callback(_REF, "FAILED", db, _CFG)

        assert tx.status == "FAILED"
        assert tx.updated_at is not None
        db.add.assert_not_called()
        mock_send.assert_called_once()
        call_args = mock_send.call_args[0]
        assert "SUBSCRIBE" in call_args[3] or "échoué" in call_args[3]

    async def test_unknown_reference_is_silently_skipped(self) -> None:
        db = _make_db(tx=None)

        with patch("tassi.payments.send_text_message", new_callable=AsyncMock) as mock_send:
            await process_payment_callback("unknown-ref", "SUCCESS", db, _CFG)

        mock_send.assert_not_called()

    async def test_already_processed_is_idempotent(self) -> None:
        tx = _mock_tx(status="SUCCESS")
        db = _make_db(tx)

        with patch("tassi.payments.send_text_message", new_callable=AsyncMock) as mock_send:
            await process_payment_callback(_REF, "SUCCESS", db, _CFG)

        assert tx.status == "SUCCESS"
        db.add.assert_not_called()
        mock_send.assert_not_called()

    async def test_send_error_is_suppressed(self) -> None:
        tx = _mock_tx()
        user = _mock_user(language="en")
        db = _make_db(tx, user)

        with patch(
            "tassi.payments.send_text_message",
            new_callable=AsyncMock,
            side_effect=Exception("meta api down"),
        ):
            # Should not raise
            await process_payment_callback(_REF, "SUCCESS", db, _CFG)

        assert tx.status == "SUCCESS"

    async def test_success_uses_user_language(self) -> None:
        tx = _mock_tx()
        user = _mock_user(language="en")
        db = _make_db(tx, user)

        with patch("tassi.payments.send_text_message", new_callable=AsyncMock) as mock_send:
            await process_payment_callback(_REF, "SUCCESS", db, _CFG)

        text = mock_send.call_args[0][3]
        assert "Tassi Plus" in text
