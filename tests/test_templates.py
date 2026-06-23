"""Tests for tassi.templates — message key parity and get_message helper."""

from tassi.templates import _REQUIRED_KEYS, MESSAGES, get_message


class TestKeyParity:
    def test_english_has_all_french_keys(self) -> None:
        assert set(MESSAGES["en"].keys()) == _REQUIRED_KEYS

    def test_pidgin_has_all_french_keys(self) -> None:
        assert set(MESSAGES["pcm"].keys()) == _REQUIRED_KEYS

    def test_no_extra_keys_in_english(self) -> None:
        assert set(MESSAGES["en"].keys()) == _REQUIRED_KEYS

    def test_no_extra_keys_in_pidgin(self) -> None:
        assert set(MESSAGES["pcm"].keys()) == _REQUIRED_KEYS


class TestGetMessage:
    def test_returns_french_for_fr(self) -> None:
        msg = get_message("fr", "ask_language")
        assert "Français" in msg

    def test_returns_english_for_en(self) -> None:
        msg = get_message("en", "ask_language")
        assert "English" in msg or "Welcome" in msg

    def test_returns_pidgin_for_pcm(self) -> None:
        msg = get_message("pcm", "ask_language")
        assert "Pidgin" in msg

    def test_unknown_language_falls_back_to_french(self) -> None:
        msg = get_message("de", "ask_language")
        assert "Français" in msg

    def test_format_placeholders_are_applied(self) -> None:
        msg = get_message("fr", "calculation_result", tax_result="129 250 XAF")
        assert "129 250 XAF" in msg

    def test_resend_result_includes_tax_result(self) -> None:
        msg = get_message("en", "resend_result", tax_result="129 250 XAF")
        assert "129 250 XAF" in msg

    def test_all_languages_have_nonempty_strings(self) -> None:
        for lang in ("fr", "en", "pcm"):
            for key in MESSAGES[lang]:
                assert MESSAGES[lang][key].strip(), f"{lang}/{key} is empty"

    def test_welcome_key_in_all_languages(self) -> None:
        for lang in ("fr", "en", "pcm"):
            msg = get_message(lang, "welcome")
            assert "Tassi" in msg
