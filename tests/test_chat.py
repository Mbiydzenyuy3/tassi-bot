"""Tests for tassi.chat — additional branch coverage for send failure path."""

from unittest.mock import patch

from tassi.chat import _detect_language, _send
from tassi.config import Settings

_CFG = Settings(
    meta_phone_number_id="p",
    meta_access_token="t",
    meta_verify_token="v",
    meta_app_secret="s",
    campay_username="u",
    campay_password="pw",
    campay_application_token="tk",
)


class TestDetectLanguage:
    def test_french_greeting_detected(self) -> None:
        assert _detect_language("bonjour") == "fr"

    def test_english_greeting_detected(self) -> None:
        assert _detect_language("hello") == "en"

    def test_pidgin_phrase_detected(self) -> None:
        assert _detect_language("abeg help me") == "pcm"

    def test_pidgin_e_no_detected(self) -> None:
        assert _detect_language("e no get") == "pcm"

    def test_numeric_only_defaults_to_french(self) -> None:
        assert _detect_language("2350000") == "fr"

    def test_unknown_text_defaults_to_french(self) -> None:
        assert _detect_language("xyz abc") == "fr"

    def test_french_wins_over_english_by_score(self) -> None:
        assert _detect_language("bonjour merci oui") == "fr"

    def test_english_wins_when_no_french_signal(self) -> None:
        assert _detect_language("hello thanks good morning") == "en"


class TestSendHelper:
    async def test_send_suppresses_exception_on_failure(self) -> None:
        """_send must not propagate httpx errors — BackgroundTasks would swallow them anyway."""
        with patch("tassi.chat.send_text_message", side_effect=Exception("network error")):
            # Should not raise
            await _send("237600000000", "fr", "ask_language", _CFG)

    async def test_send_with_format_kwargs(self) -> None:
        sent: list[str] = []

        async def fake_send(phone_id, token, msisdn, text):  # type: ignore[no-untyped-def]
            sent.append(text)

        with patch("tassi.chat.send_text_message", side_effect=fake_send):
            await _send("237600000000", "fr", "calculation_result", _CFG, tax_result="129 250 XAF")

        assert len(sent) == 1
        assert "129 250 XAF" in sent[0]
