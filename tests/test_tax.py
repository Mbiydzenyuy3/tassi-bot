"""
Exhaustive tests for tassi.tax — parse_revenue, is_zero_return, calculate_rsi,
format_tax_result.

Coverage target: 100% branch coverage on tax.py.
"""

from decimal import Decimal

from tassi.tax import (
    TaxResult,
    calculate_rsi,
    format_tax_result,
    is_zero_return,
    parse_revenue,
)


class TestParseRevenue:
    """One test per row in the Task 2.1 spec table, plus additional edge cases."""

    # ── Spec table ────────────────────────────────────────────────────────────

    def test_plain_integer(self) -> None:
        assert parse_revenue("2350000") == Decimal("2350000")

    def test_space_thousands_separator(self) -> None:
        assert parse_revenue("2 350 000") == Decimal("2350000")

    def test_dot_thousands_separator(self) -> None:
        assert parse_revenue("2.350.000") == Decimal("2350000")

    def test_comma_thousands_separator(self) -> None:
        assert parse_revenue("2,350,000") == Decimal("2350000")

    def test_frs_suffix(self) -> None:
        assert parse_revenue("2350000 frs") == Decimal("2350000")

    def test_xaf_suffix(self) -> None:
        assert parse_revenue("2 350 000 XAF") == Decimal("2350000")

    def test_dot_decimal_point(self) -> None:
        assert parse_revenue("2350000.00") == Decimal("2350000.00")

    def test_mixed_comma_thousands_dot_decimal(self) -> None:
        assert parse_revenue("1,500,000.50") == Decimal("1500000.50")

    def test_empty_string_returns_none(self) -> None:
        assert parse_revenue("") is None

    def test_alphabetic_returns_none(self) -> None:
        assert parse_revenue("abc") is None

    def test_negative_returns_none(self) -> None:
        assert parse_revenue("-1000") is None

    def test_zero_is_valid(self) -> None:
        assert parse_revenue("0") == Decimal("0")

    # ── Additional cases ─────────────────────────────────────────────────────

    def test_fcfa_suffix(self) -> None:
        assert parse_revenue("500000 fcfa") == Decimal("500000")

    def test_fr_suffix_attached(self) -> None:
        assert parse_revenue("100000fr") == Decimal("100000")

    def test_xaf_uppercase_no_space(self) -> None:
        assert parse_revenue("2350000XAF") == Decimal("2350000")

    def test_single_dot_three_digits_is_thousands(self) -> None:
        # "2.350" is 2350 in French notation, not 2.350
        assert parse_revenue("2.350") == Decimal("2350")

    def test_single_dot_two_digits_is_decimal(self) -> None:
        # "235.50" is a decimal number
        assert parse_revenue("235.50") == Decimal("235.50")

    def test_single_comma_three_digits_is_thousands(self) -> None:
        assert parse_revenue("2,350") == Decimal("2350")

    def test_single_comma_two_digits_is_decimal(self) -> None:
        assert parse_revenue("1500,50") == Decimal("1500.50")

    def test_european_format_dot_thousands_comma_decimal(self) -> None:
        # "2.350.000,50" → comma is last → decimal; dots are thousands
        assert parse_revenue("2.350.000,50") == Decimal("2350000.50")

    def test_whitespace_only_returns_none(self) -> None:
        assert parse_revenue("   ") is None

    def test_zero_decimal_string(self) -> None:
        assert parse_revenue("0.00") == Decimal("0.00")

    def test_currency_suffix_only_returns_none(self) -> None:
        # After stripping "frs", the remaining string is empty
        assert parse_revenue("frs") is None


class TestIsZeroReturn:
    """All positive and negative cases from spec and Pidgin additions (FR-TAX-3)."""

    # ── Numeric zeros ─────────────────────────────────────────────────────────

    def test_zero_string(self) -> None:
        assert is_zero_return("0") is True

    def test_zero_decimal_string(self) -> None:
        assert is_zero_return("0.00") is True

    def test_zero_frs(self) -> None:
        assert is_zero_return("0 frs") is True

    def test_zero_xaf(self) -> None:
        assert is_zero_return("0 XAF") is True

    # ── French keywords ───────────────────────────────────────────────────────

    def test_rien_lowercase(self) -> None:
        assert is_zero_return("rien") is True

    def test_rien_capitalized(self) -> None:
        assert is_zero_return("Rien") is True

    def test_rien_uppercase(self) -> None:
        assert is_zero_return("RIEN") is True

    def test_neant_with_accent(self) -> None:
        assert is_zero_return("néant") is True

    def test_neant_capitalized(self) -> None:
        assert is_zero_return("Néant") is True

    def test_neant_no_accent(self) -> None:
        assert is_zero_return("neant") is True

    # ── English keywords ──────────────────────────────────────────────────────

    def test_nothing_lowercase(self) -> None:
        assert is_zero_return("nothing") is True

    def test_nothing_capitalized(self) -> None:
        assert is_zero_return("Nothing") is True

    def test_nada(self) -> None:
        assert is_zero_return("nada") is True

    # ── Cameroonian Pidgin English keywords (FR-TAX-3) ────────────────────────

    def test_pidgin_e_no_get(self) -> None:
        assert is_zero_return("e no get") is True

    def test_pidgin_no_money(self) -> None:
        assert is_zero_return("no money") is True

    def test_pidgin_e_finish(self) -> None:
        assert is_zero_return("e finish") is True

    def test_pidgin_nothing_dey(self) -> None:
        assert is_zero_return("nothing dey") is True

    def test_pidgin_i_no_sell(self) -> None:
        assert is_zero_return("i no sell") is True

    # ── False cases ───────────────────────────────────────────────────────────

    def test_positive_number_is_false(self) -> None:
        assert is_zero_return("2350000") is False

    def test_unparseable_string_is_false(self) -> None:
        assert is_zero_return("abc") is False

    def test_one_is_false(self) -> None:
        assert is_zero_return("1") is False

    def test_small_positive_is_false(self) -> None:
        assert is_zero_return("0.01") is False


class TestCalculateRsi:
    """Every named test case from Task 2.3 spec table."""

    def test_unconfirmed_standard_revenue(self) -> None:
        r = calculate_rsi(Decimal("2350000.00"), Decimal("0.055"), "UNCONFIRMED", Decimal("0.10"))
        assert r.base_acompte == Decimal("129250.00")
        assert r.cac_amount is None
        assert r.total_due is None

    def test_additive_standard_revenue(self) -> None:
        r = calculate_rsi(Decimal("2350000.00"), Decimal("0.055"), "ADDITIVE", Decimal("0.10"))
        assert r.base_acompte == Decimal("129250.00")
        assert r.cac_amount == Decimal("12925.00")
        assert r.total_due == Decimal("142175.00")

    def test_included_standard_revenue(self) -> None:
        r = calculate_rsi(Decimal("2350000.00"), Decimal("0.055"), "INCLUDED", Decimal("0.10"))
        assert r.base_acompte == Decimal("129250.00")
        assert r.cac_amount == Decimal("0.00")
        assert r.total_due == Decimal("129250.00")

    def test_additive_1_234_567(self) -> None:
        r = calculate_rsi(Decimal("1234567.89"), Decimal("0.055"), "ADDITIVE", Decimal("0.10"))
        assert r.base_acompte == Decimal("67901.23")
        assert r.cac_amount == Decimal("6790.12")
        assert r.total_due == Decimal("74691.35")

    def test_additive_10_million(self) -> None:
        r = calculate_rsi(Decimal("10000000.00"), Decimal("0.055"), "ADDITIVE", Decimal("0.10"))
        assert r.base_acompte == Decimal("550000.00")
        assert r.cac_amount == Decimal("55000.00")
        assert r.total_due == Decimal("605000.00")

    def test_additive_50_million(self) -> None:
        r = calculate_rsi(Decimal("50000000.00"), Decimal("0.055"), "ADDITIVE", Decimal("0.10"))
        assert r.base_acompte == Decimal("2750000.00")
        assert r.cac_amount == Decimal("275000.00")
        assert r.total_due == Decimal("3025000.00")

    def test_additive_one_xaf(self) -> None:
        r = calculate_rsi(Decimal("1.00"), Decimal("0.055"), "ADDITIVE", Decimal("0.10"))
        assert r.base_acompte == Decimal("0.06")
        assert r.cac_amount == Decimal("0.01")
        assert r.total_due == Decimal("0.07")

    def test_result_carries_gross_revenue(self) -> None:
        r = calculate_rsi(Decimal("2350000"), Decimal("0.055"), "ADDITIVE", Decimal("0.10"))
        assert r.gross_revenue == Decimal("2350000")

    def test_result_carries_cac_mode(self) -> None:
        r = calculate_rsi(Decimal("2350000"), Decimal("0.055"), "ADDITIVE", Decimal("0.10"))
        assert r.cac_mode == "ADDITIVE"

    def test_result_carries_cac_rate(self) -> None:
        r = calculate_rsi(Decimal("2350000"), Decimal("0.055"), "ADDITIVE", Decimal("0.10"))
        assert r.cac_rate == Decimal("0.10")

    def test_included_cac_amount_is_zero(self) -> None:
        r = calculate_rsi(Decimal("1000000"), Decimal("0.055"), "INCLUDED", Decimal("0.10"))
        assert r.cac_amount == Decimal("0.00")

    def test_unconfirmed_total_is_none(self) -> None:
        r = calculate_rsi(Decimal("1000000"), Decimal("0.055"), "UNCONFIRMED", Decimal("0.10"))
        assert r.total_due is None


class TestRoundingPrecision:
    """Cases where float arithmetic would give wrong answers. Decimal must be used."""

    def test_half_up_on_0_055_of_one_xaf(self) -> None:
        # 1.00 * 0.055 = 0.055 -> ROUND_HALF_UP -> 0.06, not 0.05 (ROUND_HALF_EVEN)
        r = calculate_rsi(Decimal("1.00"), Decimal("0.055"), "ADDITIVE", Decimal("0.10"))
        assert r.base_acompte == Decimal("0.06")

    def test_cac_half_up_on_0_006(self) -> None:
        # 0.06 * 0.10 = 0.006 -> ROUND_HALF_UP -> 0.01
        r = calculate_rsi(Decimal("1.00"), Decimal("0.055"), "ADDITIVE", Decimal("0.10"))
        assert r.cac_amount == Decimal("0.01")

    def test_no_float_drift_on_large_fractional_revenue(self) -> None:
        # float("1234567.89") * 0.055 introduces drift; Decimal does not
        r = calculate_rsi(Decimal("1234567.89"), Decimal("0.055"), "ADDITIVE", Decimal("0.10"))
        assert r.base_acompte == Decimal("67901.23")
        assert r.cac_amount == Decimal("6790.12")

    def test_total_additively_correct(self) -> None:
        # Verify total = base + cac, no floating-point accumulation error
        r = calculate_rsi(Decimal("2350000.00"), Decimal("0.055"), "ADDITIVE", Decimal("0.10"))
        assert r.total_due == r.base_acompte + r.cac_amount  # type: ignore[operator]


class TestFormatTaxResult:
    """Both languages, all three cac_modes, and fallback behaviour."""

    @staticmethod
    def _std(cac_mode: str) -> TaxResult:
        return calculate_rsi(Decimal("2350000.00"), Decimal("0.055"), cac_mode, Decimal("0.10"))

    # ── French ────────────────────────────────────────────────────────────────

    def test_fr_additive_shows_total(self) -> None:
        msg = format_tax_result(self._std("ADDITIVE"), "fr")
        assert "Total du" in msg
        assert "142" in msg

    def test_fr_additive_shows_cac_line(self) -> None:
        msg = format_tax_result(self._std("ADDITIVE"), "fr")
        assert "CAC" in msg
        assert "12" in msg

    def test_fr_additive_header(self) -> None:
        msg = format_tax_result(self._std("ADDITIVE"), "fr")
        assert "*Calcul RSI*" in msg

    def test_fr_included_shows_inclus(self) -> None:
        msg = format_tax_result(self._std("INCLUDED"), "fr")
        assert "inclus" in msg

    def test_fr_included_shows_total(self) -> None:
        msg = format_tax_result(self._std("INCLUDED"), "fr")
        assert "Total du" in msg

    def test_fr_unconfirmed_shows_disclaimer(self) -> None:
        msg = format_tax_result(self._std("UNCONFIRMED"), "fr")
        assert "comptable" in msg

    def test_fr_unconfirmed_shows_tilde_estimate(self) -> None:
        msg = format_tax_result(self._std("UNCONFIRMED"), "fr")
        assert "~" in msg

    def test_fr_unconfirmed_shows_warning_emoji(self) -> None:
        msg = format_tax_result(self._std("UNCONFIRMED"), "fr")
        assert "⚠" in msg

    def test_fr_unconfirmed_no_total_line(self) -> None:
        msg = format_tax_result(self._std("UNCONFIRMED"), "fr")
        assert "Total" not in msg

    def test_fr_unconfirmed_shows_check_emoji(self) -> None:
        msg = format_tax_result(self._std("UNCONFIRMED"), "fr")
        assert "✓" in msg

    # ── English ───────────────────────────────────────────────────────────────

    def test_en_additive_shows_total_due(self) -> None:
        msg = format_tax_result(self._std("ADDITIVE"), "en")
        assert "Total due" in msg

    def test_en_additive_header(self) -> None:
        msg = format_tax_result(self._std("ADDITIVE"), "en")
        assert "RSI Tax Calculation" in msg

    def test_en_included_shows_included(self) -> None:
        msg = format_tax_result(self._std("INCLUDED"), "en")
        assert "included" in msg.lower()

    def test_en_unconfirmed_shows_accountant(self) -> None:
        msg = format_tax_result(self._std("UNCONFIRMED"), "en")
        assert "accountant" in msg

    def test_en_unconfirmed_shows_estimate_label(self) -> None:
        msg = format_tax_result(self._std("UNCONFIRMED"), "en")
        assert "estimate" in msg

    # ── Pidgin ────────────────────────────────────────────────────────────────

    def test_pcm_additive_header(self) -> None:
        msg = format_tax_result(self._std("ADDITIVE"), "pcm")
        assert "*RSI Tax*" in msg

    def test_pcm_additive_shows_pay(self) -> None:
        msg = format_tax_result(self._std("ADDITIVE"), "pcm")
        assert "pay" in msg.lower()

    def test_pcm_included_shows_include(self) -> None:
        msg = format_tax_result(self._std("INCLUDED"), "pcm")
        assert "include" in msg.lower()

    def test_pcm_unconfirmed_shows_accountant(self) -> None:
        msg = format_tax_result(self._std("UNCONFIRMED"), "pcm")
        assert "accountant" in msg

    def test_pcm_unconfirmed_shows_estimate(self) -> None:
        msg = format_tax_result(self._std("UNCONFIRMED"), "pcm")
        assert "estimate" in msg

    # ── Fallback ──────────────────────────────────────────────────────────────

    def test_unknown_language_falls_back_to_french(self) -> None:
        msg = format_tax_result(self._std("ADDITIVE"), "es")
        assert "Total du" in msg  # French label fallback
