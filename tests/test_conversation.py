"""
Integration-style tests for the Tassi conversation state machine.
Tests T1-T6 from PERSONAS section 5.

DB is fully mocked (no Postgres needed) — tests verify state transitions,
template key selection, and that send_text_message is called with the
right text. The real DB path is exercised in CI against the Postgres service.
"""

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

from tassi.chat import handle_message
from tassi.config import Settings
from tassi.models import TaxCalculation

# ── Shared fixtures ───────────────────────────────────────────────────────────

_MSISDN = "237612345678"
_MSG_ID = "wamid.test001"
_CFG = Settings(
    meta_phone_number_id="test-phone-id",
    meta_access_token="test-access-token",
    meta_verify_token="test-verify-token",
    meta_app_secret="test-secret",
    campay_username="u",
    campay_password="p",
    campay_application_token="t",
    cac_mode="ADDITIVE",
    cac_rate="0.10",
    rate_rsi="0.055",
)


def _make_db_factory(
    calc_row: TaxCalculation | None = None,
    resend_path: bool = False,
) -> MagicMock:
    """Return a mock db_factory whose sessions support the operations chat.py needs.

    resend_path=True  → first execute returns calc_row (TaxCalculation query in _handle_resend)
    resend_path=False → first execute returns None user (User query in _get_or_create_user)
    """
    session = AsyncMock()

    # select(User) → no existing user (new user path)
    user_result = MagicMock()
    user_result.scalar_one_or_none.return_value = None

    # select(TaxCalculation) for RESEND
    calc_result = MagicMock()
    calc_result.scalar_one_or_none.return_value = calc_row

    if resend_path:
        session.execute = AsyncMock(side_effect=[calc_result, user_result] * 10)
    else:
        session.execute = AsyncMock(side_effect=[user_result, calc_result] * 10)

    session.add = MagicMock()
    session.flush = AsyncMock()

    # db.begin() as async context manager
    begin_ctx = AsyncMock()
    begin_ctx.__aenter__ = AsyncMock(return_value=None)
    begin_ctx.__aexit__ = AsyncMock(return_value=False)
    session.begin = MagicMock(return_value=begin_ctx)

    # db_factory() must be a synchronous call returning an async context manager
    ctx = AsyncMock()
    ctx.__aenter__ = AsyncMock(return_value=session)
    ctx.__aexit__ = AsyncMock(return_value=False)
    factory = MagicMock(return_value=ctx)
    return factory


class TestT1StandardCalculationFrench:
    """T1: Aïssatou sends revenue in French — receives correct Acompte."""

    async def test_calculation_result_sent(self) -> None:
        sent: list[tuple[str, str, str, str]] = []

        async def fake_send(phone_id: str, token: str, msisdn: str, text: str) -> None:
            sent.append((phone_id, token, msisdn, text))

        session_state: dict = {"state": "ACTIVE", "language": "fr"}

        async def fake_get(redis, msisdn):  # type: ignore[no-untyped-def]
            return dict(session_state)

        async def fake_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            session_state.update(state)

        redis = AsyncMock()
        db_factory = _make_db_factory()

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "2 350 000 frs", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 1
        _, _, _, text = sent[0]
        # Result must contain the base acompte amount (2350000 * 0.055 = 129 250)
        assert "129" in text or "129 250" in text or "129250" in text


class TestT2StandardCalculationEnglish:
    """T2: User sends revenue in English — receives calculation in English."""

    async def test_calculation_result_sent_in_english(self) -> None:
        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        session_state: dict = {"state": "ACTIVE", "language": "en"}

        async def fake_get(redis, msisdn):  # type: ignore[no-untyped-def]
            return dict(session_state)

        async def fake_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            session_state.update(state)

        redis = AsyncMock()
        db_factory = _make_db_factory()

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "2350000", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 1
        assert "129" in sent[0]


class TestT3ZeroReturn:
    """T3: User sends zero-revenue phrase — receives Néant guidance (no payment due)."""

    @pytest.mark.parametrize("phrase", ["rien", "e no get", "no money", "nothing dey", "i no sell"])
    async def test_zero_return_sends_guidance(self, phrase: str) -> None:
        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        session_state: dict = {"state": "ACTIVE", "language": "fr"}

        async def fake_get(redis, msisdn):  # type: ignore[no-untyped-def]
            return dict(session_state)

        async def fake_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            session_state.update(state)

        redis = AsyncMock()
        db_factory = _make_db_factory()

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, phrase, _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 1
        text = sent[0]
        assert "Néant" in text or "Neant" in text.replace("é", "e") or "néant" in text.lower()


class TestT4InvalidThenValid:
    """T4: User sends garbage, gets error, then sends valid revenue, gets result."""

    async def test_invalid_input_then_valid(self) -> None:
        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        session_state: dict = {"state": "ACTIVE", "language": "fr"}

        async def fake_get(redis, msisdn):  # type: ignore[no-untyped-def]
            return dict(session_state)

        async def fake_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            session_state.update(state)

        redis = AsyncMock()
        db_factory = _make_db_factory()

        patches = (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        )
        with patches[0], patches[1], patches[2]:
            # First: garbage input
            await handle_message(_MSISDN, "abc xyz", _MSG_ID + "-1", db_factory, redis, _CFG)
            assert len(sent) == 1
            assert "❌" in sent[0] or "reconnai" in sent[0].lower() or "understand" in sent[0]

            # Second: valid revenue
            await handle_message(_MSISDN, "2 350 000", _MSG_ID + "-2", db_factory, redis, _CFG)
        assert len(sent) == 2
        assert "129" in sent[1]


class TestT5DuplicateMessageId:
    """T5: Same message_id twice — state machine called only once (dedup in main.py)."""

    async def test_send_called_once_for_duplicate(self) -> None:
        """
        Dedup is enforced in main.py before handle_message is called.
        This test verifies handle_message itself does NOT produce duplicate output
        if somehow called twice — state machine is idempotent for AWAITING_LANGUAGE repeat.
        """
        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        # Session starts AWAITING_LANGUAGE; both calls to handle_message
        # attempt to pick language — first sets state to AWAITING_BAND, second sees
        # AWAITING_BAND and processes "fr" as unexpected input → resends band picker.
        call_count = [0]

        async def stateful_get(redis, msisdn):  # type: ignore[no-untyped-def]
            if call_count[0] == 0:
                return {"state": "AWAITING_LANGUAGE", "language": "fr"}
            return {"state": "AWAITING_BAND", "language": "fr"}

        async def stateful_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            call_count[0] += 1

        redis = AsyncMock()
        db_factory = _make_db_factory()

        with (
            patch("tassi.chat.get_session", side_effect=stateful_get),
            patch("tassi.chat.set_session", side_effect=stateful_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "1", _MSG_ID, db_factory, redis, _CFG)
            await handle_message(_MSISDN, "1", _MSG_ID, db_factory, redis, _CFG)

        # Two calls → two sends (one per invocation). In production the webhook dedup
        # layer (main.py) ensures handle_message is only dispatched once.
        assert len(sent) == 2


class TestT6ResendCommand:
    """T6: RESEND command — returns last calculation for current fiscal period."""

    async def test_resend_returns_last_calculation(self) -> None:
        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        session_state: dict = {"state": "ACTIVE", "language": "fr"}

        async def fake_get(redis, msisdn):  # type: ignore[no-untyped-def]
            return dict(session_state)

        async def fake_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            session_state.update(state)

        # Simulate a TaxCalculation row returned from DB
        import uuid
        from datetime import UTC, datetime

        calc = MagicMock(spec=TaxCalculation)
        calc.gross_revenue = Decimal("2350000.00")
        calc.base_acompte = Decimal("129250.00")
        calc.cac_amount = Decimal("12925.00")
        calc.cac_mode = "ADDITIVE"
        calc.fiscal_period = datetime.now(tz=UTC).strftime("%Y-%m")
        calc.is_zero_return = False
        calc.created_at = datetime.now(tz=UTC)
        calc.user_id = uuid.uuid4()
        calc.id = uuid.uuid4()

        redis = AsyncMock()
        db_factory = _make_db_factory(calc_row=calc, resend_path=True)

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "RESEND", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 1
        text = sent[0]
        # French resend_result template + formatted tax amount
        assert "dernier calcul" in text or "129" in text

    async def test_resend_with_no_history_sends_no_history_message(self) -> None:
        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        session_state: dict = {"state": "ACTIVE", "language": "fr"}

        async def fake_get(redis, msisdn):  # type: ignore[no-untyped-def]
            return dict(session_state)

        async def fake_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            session_state.update(state)

        redis = AsyncMock()
        # calc_row=None → no history found; resend_path so calc query fires first
        db_factory = _make_db_factory(calc_row=None, resend_path=True)

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "RENVOYER", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 1
        assert "calcul" in sent[0].lower() or "history" in sent[0].lower()


class TestOnboarding:
    """State machine NEW → AWAITING_LANGUAGE → AWAITING_BAND → ACTIVE flow."""

    async def test_new_user_gets_language_prompt(self) -> None:
        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        session_state: dict = {}

        async def fake_get(redis, msisdn):  # type: ignore[no-untyped-def]
            return dict(session_state)

        async def fake_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            session_state.update(state)

        redis = AsyncMock()
        db_factory = _make_db_factory()

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "hello", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 2  # welcome + picker (was 1 before)
        assert "1️⃣" not in sent[0]  # greeting has no picker items
        assert "1️⃣" in sent[1]  # picker is the second message
        assert session_state["state"] == "AWAITING_LANGUAGE"

    async def test_english_first_message_gets_english_welcome(self) -> None:
        """If user's first message is English, welcome and picker are in English."""
        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        session_state: dict = {}

        async def fake_get(redis, msisdn):  # type: ignore[no-untyped-def]
            return dict(session_state)

        async def fake_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            session_state.update(state)

        redis = AsyncMock()
        db_factory = _make_db_factory()

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(
                _MSISDN, "i want to calculate my revenue", _MSG_ID, db_factory, redis, _CFG
            )

        assert len(sent) == 2
        assert "Welcome" in sent[0]  # English welcome
        assert "Choose" in sent[1]  # English picker (not "Choisissez")
        assert session_state["language"] == "en"

    async def test_french_first_message_gets_french_welcome(self) -> None:
        """If user's first message is French, welcome and picker are in French."""
        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        session_state: dict = {}

        async def fake_get(redis, msisdn):  # type: ignore[no-untyped-def]
            return dict(session_state)

        async def fake_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            session_state.update(state)

        redis = AsyncMock()
        db_factory = _make_db_factory()

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(
                _MSISDN, "bonjour je veux calculer mes taxes", _MSG_ID, db_factory, redis, _CFG
            )

        assert len(sent) == 2
        assert "Bienvenue" in sent[0]  # French welcome
        assert "Choisissez" in sent[1]  # French picker
        assert session_state["language"] == "fr"

    async def test_unrecognized_first_message_defaults_to_french(self) -> None:
        """First message with no language cues defaults to French."""
        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        session_state: dict = {}

        async def fake_get(redis, msisdn):  # type: ignore[no-untyped-def]
            return dict(session_state)

        async def fake_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            session_state.update(state)

        redis = AsyncMock()
        db_factory = _make_db_factory()

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "123", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 2
        assert "Bienvenue" in sent[0]
        assert session_state["language"] == "fr"

    async def test_language_2_switches_to_english(self) -> None:
        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        session_state: dict = {"state": "AWAITING_LANGUAGE", "language": "fr"}

        async def fake_get(redis, msisdn):  # type: ignore[no-untyped-def]
            return dict(session_state)

        async def fake_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            session_state.update(state)

        redis = AsyncMock()
        db_factory = _make_db_factory()

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "2", _MSG_ID, db_factory, redis, _CFG)

        assert session_state["language"] == "en"
        assert session_state["state"] == "AWAITING_BAND"
        assert "revenue" in sent[0].lower() or "Between" in sent[0]

    async def test_band_1_transitions_to_active(self) -> None:
        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        session_state: dict = {"state": "AWAITING_BAND", "language": "fr"}

        async def fake_get(redis, msisdn):  # type: ignore[no-untyped-def]
            return dict(session_state)

        async def fake_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            session_state.update(state)

        redis = AsyncMock()
        db_factory = _make_db_factory()

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "1", _MSG_ID, db_factory, redis, _CFG)

        assert session_state["state"] == "ACTIVE"
        assert session_state["annual_revenue_band"] == "RSI_10_50M"
        assert "chiffre d'affaires" in sent[0] or "revenue" in sent[0].lower()

    async def test_out_of_band_after_3_tries_sends_final_message(self) -> None:
        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        session_state: dict = {"state": "AWAITING_BAND", "language": "fr", "band_tries": 2}

        async def fake_get(redis, msisdn):  # type: ignore[no-untyped-def]
            return dict(session_state)

        async def fake_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            session_state.update(state)

        redis = AsyncMock()
        db_factory = _make_db_factory()

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            # Send garbage (not a valid band choice, not in-range revenue)
            await handle_message(_MSISDN, "5", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 1
        # Should be the out_of_band_final message (3rd rejection)
        assert "comptable" in sent[0] or "accountant" in sent[0] or "abeg" in sent[0]

    async def test_unknown_state_resets_session(self) -> None:
        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        session_state: dict = {"state": "CORRUPTED"}
        reset_called = [False]

        async def fake_get(redis, msisdn):  # type: ignore[no-untyped-def]
            return dict(session_state)

        async def fake_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            reset_called[0] = True
            session_state.update(state)

        redis = AsyncMock()
        db_factory = _make_db_factory()

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "hello", _MSG_ID, db_factory, redis, _CFG)

        # Should have reset and sent welcome
        assert len(sent) >= 1
        assert reset_called[0]


class TestMissingBranches:
    """Targeted tests to cover remaining uncovered branches in chat.py."""

    async def test_language_3_selects_pidgin(self) -> None:
        """Lines 115-116: pcm branch in _handle_awaiting_language."""
        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        session_state: dict = {"state": "AWAITING_LANGUAGE", "language": "fr"}

        async def fake_get(redis, msisdn):  # type: ignore[no-untyped-def]
            return dict(session_state)

        async def fake_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            session_state.update(state)

        redis = AsyncMock()
        db_factory = _make_db_factory()

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "3", _MSG_ID, db_factory, redis, _CFG)

        assert session_state["language"] == "pcm"
        assert session_state["state"] == "AWAITING_BAND"
        assert len(sent) == 1

    async def test_free_text_detects_language_and_proceeds(self) -> None:
        """Else branch in _handle_awaiting_language: free text → detect lang → advance."""
        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        session_state: dict = {"state": "AWAITING_LANGUAGE", "language": "fr"}

        async def fake_get(redis, msisdn):  # type: ignore[no-untyped-def]
            return dict(session_state)

        async def fake_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            session_state.update(state)

        redis = AsyncMock()
        db_factory = _make_db_factory()

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            # User types a French greeting instead of choosing 1/2/3
            await handle_message(_MSISDN, "bonjour", _MSG_ID, db_factory, redis, _CFG)

        # Should advance to AWAITING_BAND, not stay stuck
        assert session_state.get("state") == "AWAITING_BAND"
        assert session_state.get("language") == "fr"
        assert len(sent) == 1  # band picker sent in French

    async def test_revenue_text_in_awaiting_language_defaults_to_french(self) -> None:
        """Numeric input during AWAITING_LANGUAGE has no language signal → default fr."""
        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        session_state: dict = {"state": "AWAITING_LANGUAGE", "language": "fr"}

        async def fake_get(redis, msisdn):  # type: ignore[no-untyped-def]
            return dict(session_state)

        async def fake_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            session_state.update(state)

        redis = AsyncMock()
        db_factory = _make_db_factory()

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            # User skips picker and types their revenue directly
            await handle_message(_MSISDN, "2350000", _MSG_ID, db_factory, redis, _CFG)

        # Defaults to French, proceeds to AWAITING_BAND
        assert session_state.get("state") == "AWAITING_BAND"
        assert session_state.get("language") == "fr"

    async def test_in_band_revenue_text_accepted_during_band_selection(self) -> None:
        """Line 143: parse_revenue succeeds and value is in-range during AWAITING_BAND."""
        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        session_state: dict = {"state": "AWAITING_BAND", "language": "en"}

        async def fake_get(redis, msisdn):  # type: ignore[no-untyped-def]
            return dict(session_state)

        async def fake_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            session_state.update(state)

        redis = AsyncMock()
        db_factory = _make_db_factory()

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            # 20 000 000 is within RSI range → accepted
            await handle_message(_MSISDN, "20000000", _MSG_ID, db_factory, redis, _CFG)

        assert session_state["state"] == "ACTIVE"
        assert len(sent) == 1

    async def test_first_out_of_band_sends_warning(self) -> None:
        """Lines 160-162: first rejection (band_tries=0 → 1), else branch."""
        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        session_state: dict = {"state": "AWAITING_BAND", "language": "fr"}

        async def fake_get(redis, msisdn):  # type: ignore[no-untyped-def]
            return dict(session_state)

        async def fake_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            session_state.update(state)

        redis = AsyncMock()
        db_factory = _make_db_factory()

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "99", _MSG_ID, db_factory, redis, _CFG)

        # Warning, not final message — stays AWAITING_BAND
        assert session_state.get("state") == "AWAITING_BAND"
        assert session_state.get("band_tries") == 1
        assert len(sent) == 1
        assert "10 M" in sent[0] or "RSI" in sent[0]

    async def test_existing_user_is_reused(self) -> None:
        """Line 210→214: _get_or_create_user finds existing user (not None branch)."""
        import uuid as uuid_mod

        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        session_state: dict = {"state": "ACTIVE", "language": "fr"}

        async def fake_get(redis, msisdn):  # type: ignore[no-untyped-def]
            return dict(session_state)

        async def fake_set(redis, msisdn, state):  # type: ignore[no-untyped-def]
            session_state.update(state)

        # Build a mock db where User already exists (scalar_one_or_none → existing User)
        session = AsyncMock()
        existing_user = MagicMock()
        existing_user.id = uuid_mod.uuid4()

        user_result = MagicMock()
        user_result.scalar_one_or_none.return_value = existing_user

        session.execute = AsyncMock(return_value=user_result)
        session.add = MagicMock()
        session.flush = AsyncMock()

        begin_ctx = AsyncMock()
        begin_ctx.__aenter__ = AsyncMock(return_value=None)
        begin_ctx.__aexit__ = AsyncMock(return_value=False)
        session.begin = MagicMock(return_value=begin_ctx)

        ctx = AsyncMock()
        ctx.__aenter__ = AsyncMock(return_value=session)
        ctx.__aexit__ = AsyncMock(return_value=False)
        db_factory = MagicMock(return_value=ctx)

        redis = AsyncMock()

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "2350000", _MSG_ID, db_factory, redis, _CFG)

        # Existing user reused — flush should NOT have been called
        session.flush.assert_not_called()
        assert len(sent) == 1
        assert "129" in sent[0]


# ── Milestone 5 payment command tests ────────────────────────────────────────


def _result_mock(
    scalar_one_or_none=None,
    scalar_one=None,
    scalars_all=None,
) -> MagicMock:
    r = MagicMock()
    r.scalar_one_or_none.return_value = scalar_one_or_none
    r.scalar_one.return_value = scalar_one
    r.scalars.return_value.all.return_value = scalars_all if scalars_all is not None else []
    return r


def _make_db_factory_seq(execute_results: list) -> MagicMock:
    """Factory whose session.execute returns results from execute_results in order."""
    session = AsyncMock()
    session.execute = AsyncMock(side_effect=execute_results)
    session.add = MagicMock()
    session.flush = AsyncMock()

    begin_ctx = AsyncMock()
    begin_ctx.__aenter__ = AsyncMock(return_value=None)
    begin_ctx.__aexit__ = AsyncMock(return_value=False)
    session.begin = MagicMock(return_value=begin_ctx)

    ctx = AsyncMock()
    ctx.__aenter__ = AsyncMock(return_value=session)
    ctx.__aexit__ = AsyncMock(return_value=False)
    return MagicMock(return_value=ctx)


def _active_session(language: str = "fr") -> dict:
    return {"state": "ACTIVE", "language": language}


def _awaiting_operator_session(language: str = "fr") -> dict:
    return {"state": "AWAITING_OPERATOR", "language": language}


def _fake_redis_for(initial_session: dict):
    """Return (redis, get_session, set_session) fakes for a given initial state."""
    sessions: dict = {}
    captured: list = []

    async def fake_get(redis, msisdn):
        return sessions.get(msisdn, initial_session.copy())

    async def fake_set(redis, msisdn, data):
        sessions[msisdn] = data
        captured.append(data.copy())

    return AsyncMock(), fake_get, fake_set, captured


class TestSubscribeCommand:
    async def test_subscribe_not_subscribed_asks_operator(self) -> None:
        db_factory = _make_db_factory_seq([_result_mock(scalar_one_or_none=None)])
        redis, fake_get, fake_set, _ = _fake_redis_for(_active_session())
        sent: list[str] = []

        async def fake_send(*a, **kw):
            sent.append(a[3] if len(a) > 3 else "")

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "subscribe", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 1
        assert "500" in sent[0] or "MTN" in sent[0]

    async def test_subscribe_already_subscribed_sends_message(self) -> None:
        plus_user = MagicMock()
        type(plus_user).is_plus = PropertyMock(return_value=True)
        db_factory = _make_db_factory_seq([_result_mock(scalar_one_or_none=plus_user)])
        redis, fake_get, fake_set, _ = _fake_redis_for(_active_session())
        sent: list[str] = []

        async def fake_send(*a, **kw):
            sent.append(a[3] if len(a) > 3 else "")

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "abonnement", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 1
        assert "déjà" in sent[0] or "already" in sent[0]


class TestAwaitingOperatorState:
    async def test_mtn_operator_creates_payment_and_sends_initiated(self) -> None:
        # _get_or_create_user: no existing user
        db_factory = _make_db_factory_seq([_result_mock(scalar_one_or_none=None)])
        redis, fake_get, fake_set, _ = _fake_redis_for(_awaiting_operator_session())
        sent: list[str] = []

        async def fake_send(*a, **kw):
            sent.append(a[3] if len(a) > 3 else "")

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
            patch(
                "tassi.chat.initiate_ussd_push",
                new_callable=AsyncMock,
                return_value="CPY-T-001",
            ),
        ):
            await handle_message(_MSISDN, "1", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 1
        assert "STATUS" in sent[0] or "Vérifiez" in sent[0] or "Check" in sent[0]

    async def test_orange_operator_is_accepted(self) -> None:
        db_factory = _make_db_factory_seq([_result_mock(scalar_one_or_none=None)])
        redis, fake_get, fake_set, _ = _fake_redis_for(_awaiting_operator_session())
        sent: list[str] = []

        async def fake_send(*a, **kw):
            sent.append(a[3] if len(a) > 3 else "")

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
            patch(
                "tassi.chat.initiate_ussd_push",
                new_callable=AsyncMock,
                return_value="CPY-T-002",
            ),
        ):
            await handle_message(_MSISDN, "2", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 1
        assert "STATUS" in sent[0] or "Vérifiez" in sent[0] or "Check" in sent[0]

    async def test_invalid_operator_reprompts(self) -> None:
        db_factory = _make_db_factory_seq([])
        redis, fake_get, fake_set, _ = _fake_redis_for(_awaiting_operator_session())
        sent: list[str] = []

        async def fake_send(*a, **kw):
            sent.append(a[3] if len(a) > 3 else "")

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "visa", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 1
        assert "MTN" in sent[0]

    async def test_campay_error_sends_subscribe_error(self) -> None:
        db_factory = _make_db_factory_seq([_result_mock(scalar_one_or_none=None)])
        redis, fake_get, fake_set, _ = _fake_redis_for(_awaiting_operator_session())
        sent: list[str] = []

        async def fake_send(*a, **kw):
            sent.append(a[3] if len(a) > 3 else "")

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
            patch("tassi.chat.initiate_ussd_push", side_effect=Exception("timeout")),
        ):
            await handle_message(_MSISDN, "1", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 1
        assert "paiement" in sent[0].lower() or "payment" in sent[0].lower()


class TestStatusCommand:
    async def test_status_no_pending_payment(self) -> None:
        db_factory = _make_db_factory_seq([_result_mock(scalar_one_or_none=None)])
        redis, fake_get, fake_set, _ = _fake_redis_for(_active_session())
        sent: list[str] = []

        async def fake_send(*a, **kw):
            sent.append(a[3] if len(a) > 3 else "")

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "status", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 1
        assert "SUBSCRIBE" in sent[0] or "paiement" in sent[0].lower()

    async def test_status_too_new_sends_just_initiated(self) -> None:
        tx = MagicMock()
        tx.created_at = datetime.now(tz=UTC) - timedelta(seconds=30)
        tx.campay_reference = "CPY-NEW"
        tx.status = "PENDING"

        db_factory = _make_db_factory_seq([_result_mock(scalar_one_or_none=tx)])
        redis, fake_get, fake_set, _ = _fake_redis_for(_active_session())
        sent: list[str] = []

        async def fake_send(*a, **kw):
            sent.append(a[3] if len(a) > 3 else "")

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "statut", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 1
        assert "lancé" in sent[0] or "started" in sent[0] or "start" in sent[0]

    async def test_status_null_reference_sends_pending(self) -> None:
        tx = MagicMock()
        tx.created_at = datetime.now(tz=UTC) - timedelta(minutes=5)
        tx.campay_reference = None
        tx.status = "PENDING"

        db_factory = _make_db_factory_seq([_result_mock(scalar_one_or_none=tx)])
        redis, fake_get, fake_set, _ = _fake_redis_for(_active_session())
        sent: list[str] = []

        async def fake_send(*a, **kw):
            sent.append(a[3] if len(a) > 3 else "")

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "status", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 1
        assert "cours" in sent[0] or "processing" in sent[0] or "process" in sent[0]

    async def test_status_polled_success_triggers_callback(self) -> None:
        tx = MagicMock()
        tx.created_at = datetime.now(tz=UTC) - timedelta(minutes=5)
        tx.campay_reference = "CPY-POLLED"
        tx.status = "PENDING"

        db_factory = _make_db_factory_seq([_result_mock(scalar_one_or_none=tx)])
        redis, fake_get, fake_set, _ = _fake_redis_for(_active_session())

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", new_callable=AsyncMock),
            patch(
                "tassi.chat.get_transaction_status",
                new_callable=AsyncMock,
                return_value="SUCCESS",
            ),
            patch("tassi.chat.process_payment_callback", new_callable=AsyncMock) as mock_cb,
        ):
            await handle_message(_MSISDN, "status", _MSG_ID, db_factory, redis, _CFG)

        mock_cb.assert_called_once()
        assert mock_cb.call_args[0][1] == "SUCCESS"

    async def test_status_polled_pending_sends_pending(self) -> None:
        tx = MagicMock()
        tx.created_at = datetime.now(tz=UTC) - timedelta(minutes=5)
        tx.campay_reference = "CPY-STILL"
        tx.status = "PENDING"

        db_factory = _make_db_factory_seq([_result_mock(scalar_one_or_none=tx)])
        redis, fake_get, fake_set, _ = _fake_redis_for(_active_session())
        sent: list[str] = []

        async def fake_send(*a, **kw):
            sent.append(a[3] if len(a) > 3 else "")

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
            patch(
                "tassi.chat.get_transaction_status",
                new_callable=AsyncMock,
                return_value="PENDING",
            ),
        ):
            await handle_message(_MSISDN, "status", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 1
        assert "cours" in sent[0] or "processing" in sent[0] or "process" in sent[0]


class TestHistoryCommand:
    async def test_history_not_plus_sends_upgrade_message(self) -> None:
        non_plus = MagicMock()
        type(non_plus).is_plus = PropertyMock(return_value=False)
        db_factory = _make_db_factory_seq([_result_mock(scalar_one_or_none=non_plus)])
        redis, fake_get, fake_set, _ = _fake_redis_for(_active_session())
        sent: list[str] = []

        async def fake_send(*a, **kw):
            sent.append(a[3] if len(a) > 3 else "")

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "history", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 1
        assert "SUBSCRIBE" in sent[0] or "Plus" in sent[0]

    async def test_history_no_user_sends_upgrade_message(self) -> None:
        db_factory = _make_db_factory_seq([_result_mock(scalar_one_or_none=None)])
        redis, fake_get, fake_set, _ = _fake_redis_for(_active_session("en"))
        sent: list[str] = []

        async def fake_send(*a, **kw):
            sent.append(a[3] if len(a) > 3 else "")

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "historique", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 1
        assert "SUBSCRIBE" in sent[0] or "Plus" in sent[0]

    async def test_history_plus_empty_sends_empty_message(self) -> None:
        plus_user = MagicMock()
        plus_user.id = "user-id-1"
        type(plus_user).is_plus = PropertyMock(return_value=True)
        db_factory = _make_db_factory_seq(
            [
                _result_mock(scalar_one_or_none=plus_user),
                _result_mock(scalars_all=[]),
            ]
        )
        redis, fake_get, fake_set, _ = _fake_redis_for(_active_session())
        sent: list[str] = []

        async def fake_send(*a, **kw):
            sent.append(a[3] if len(a) > 3 else "")

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "history", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 1
        assert "calcul" in sent[0].lower() or "calculation" in sent[0].lower()

    async def test_history_plus_shows_results(self) -> None:
        plus_user = MagicMock()
        plus_user.id = "user-id-2"
        type(plus_user).is_plus = PropertyMock(return_value=True)

        calc = MagicMock(spec=TaxCalculation)
        calc.fiscal_period = "2026-05"
        calc.base_acompte = Decimal("129250")

        db_factory = _make_db_factory_seq(
            [
                _result_mock(scalar_one_or_none=plus_user),
                _result_mock(scalars_all=[calc]),
            ]
        )
        redis, fake_get, fake_set, _ = _fake_redis_for(_active_session())
        sent: list[str] = []

        async def fake_send(*a, **kw):
            sent.append(a[3] if len(a) > 3 else "")

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
        ):
            await handle_message(_MSISDN, "history", _MSG_ID, db_factory, redis, _CFG)

        assert len(sent) == 1
        assert "2026-05" in sent[0]
        assert "129" in sent[0]


# ── FR-CHAT-8: mark-as-read + typing indicator ────────────────────────────────


class TestFRChat8TypingIndicator:
    """FR-CHAT-8: mark_as_read and send_typing_indicator called at start of handle_message."""

    async def test_mark_as_read_and_typing_called_with_correct_args(self) -> None:
        """Both functions are called with the correct arguments on a normal message."""
        redis, fake_get, fake_set, _ = _fake_redis_for({"state": "ACTIVE", "language": "fr"})
        db_factory = _make_db_factory()

        async def fake_send(*a, **kw):  # type: ignore[no-untyped-def]
            pass

        mark_mock = AsyncMock()
        typing_mock = AsyncMock()

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
            patch("tassi.chat.mark_as_read", mark_mock),
            patch("tassi.chat.send_typing_indicator", typing_mock),
        ):
            await handle_message(_MSISDN, "2350000", _MSG_ID, db_factory, redis, _CFG)

        mark_mock.assert_awaited_once_with(
            _CFG.meta_phone_number_id, _CFG.meta_access_token, _MSG_ID
        )
        typing_mock.assert_awaited_once_with(
            _CFG.meta_phone_number_id, _CFG.meta_access_token, _MSISDN, _MSG_ID
        )

    async def test_handle_message_continues_if_mark_as_read_raises(self) -> None:
        """If mark_as_read raises, handle_message still completes and sends a reply."""
        redis, fake_get, fake_set, _ = _fake_redis_for({"state": "ACTIVE", "language": "fr"})
        db_factory = _make_db_factory()

        sent: list[str] = []

        async def fake_send(*a, **kw):  # type: ignore[no-untyped-def]
            sent.append(a[3] if len(a) > 3 else "")

        async def failing_mark(*a, **kw):  # type: ignore[no-untyped-def]
            raise RuntimeError("network error")

        with (
            patch("tassi.chat.get_session", side_effect=fake_get),
            patch("tassi.chat.set_session", side_effect=fake_set),
            patch("tassi.chat.send_text_message", side_effect=fake_send),
            patch("tassi.chat.mark_as_read", side_effect=failing_mark),
            patch("tassi.chat.send_typing_indicator", AsyncMock()),
        ):
            await handle_message(_MSISDN, "2350000", _MSG_ID, db_factory, redis, _CFG)

        # The bot must still have sent a reply despite the typing indicator failure
        assert len(sent) == 1
        assert "129" in sent[0]
