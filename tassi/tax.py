"""
Pure tax-calculation functions for Cameroon RSI (Regime Simplifie d'Imposition).
No database, no HTTP, no I/O -- input goes in, output comes out.
"""

import re
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Final, cast

# ── Revenue parsing ──────────────────────────────────────────────────────────

_CURRENCY_RE: Final = re.compile(
    r"\s*(fcfa|xaf|frs|fr)\s*$",
    re.IGNORECASE,
)
# \s matches all Unicode whitespace in Python 3 (including non-breaking spaces)
_SPACE_RE: Final = re.compile(r"\s+")

_TWO_PLACES: Final = Decimal("0.01")


def parse_revenue(raw: str) -> Decimal | None:
    """
    Convert a user-entered revenue string to Decimal.
    Returns None if the string cannot be parsed as a non-negative number.
    Zero is valid -- it represents the Neant (zero-return) path.
    """
    s = raw.strip()
    if not s:
        return None

    # Strip currency suffix (frs, XAF, FCFA, FR) before parsing
    s = _CURRENCY_RE.sub("", s).strip()

    if s.startswith("-"):
        return None

    # Remove all whitespace -- used as a thousands separator in French locale
    s = _SPACE_RE.sub("", s)

    if not s:
        return None

    dot_count = s.count(".")
    comma_count = s.count(",")

    if dot_count == 0 and comma_count == 0:
        pass  # plain integer -- no separator handling needed

    elif dot_count > 1 and comma_count == 0:
        # Multiple dots -> all are thousands separators ("2.350.000" -> 2350000)
        s = s.replace(".", "")

    elif comma_count > 1 and dot_count == 0:
        # Multiple commas -> all are thousands separators ("2,350,000" -> 2350000)
        s = s.replace(",", "")

    elif dot_count == 1 and comma_count == 0:
        # Single dot: if exactly 3 digits follow it is a thousands separator,
        # otherwise it is a decimal point ("2.350" -> 2350; "235.50" -> 235.50)
        after = s[s.index(".") + 1 :]
        if len(after) == 3 and after.isdigit():
            s = s.replace(".", "")

    elif comma_count == 1 and dot_count == 0:
        # Single comma: same logic -- "2,350" is thousands; "235,50" is decimal
        after = s[s.index(",") + 1 :]
        if len(after) == 3 and after.isdigit():
            s = s.replace(",", "")
        else:
            s = s.replace(",", ".")

    else:
        # Both separators present: whichever comes last is the decimal point
        # ("1,500,000.50" -> commas are thousands; "2.350.000,50" -> dots are thousands)
        if s.rfind(".") > s.rfind(","):
            s = s.replace(",", "")
        else:
            s = s.replace(".", "").replace(",", ".")

    try:
        value = Decimal(s)
    except Exception:
        return None

    return None if value < 0 else value


# ── Zero-return detection ────────────────────────────────────────────────────

_ZERO_KEYWORDS: Final = frozenset(
    {
        # French
        "rien",
        "neant",
        "néant",
        # English
        "nothing",
        "nada",
        # Cameroonian Pidgin English (FR-TAX-3)
        "e no get",
        "no money",
        "e finish",
        "nothing dey",
        "i no sell",
    }
)


def is_zero_return(raw: str) -> bool:
    """Return True if the input indicates zero revenue for the period."""
    if raw.strip().lower() in _ZERO_KEYWORDS:
        return True
    parsed = parse_revenue(raw)
    return parsed is not None and parsed == Decimal("0")


# ── RSI calculation ──────────────────────────────────────────────────────────


@dataclass(frozen=True)
class TaxResult:
    gross_revenue: Decimal
    base_acompte: Decimal
    cac_amount: Decimal | None  # None when cac_mode is UNCONFIRMED
    cac_mode: str  # "ADDITIVE" | "INCLUDED" | "UNCONFIRMED"
    cac_rate: Decimal  # always set; used by formatter for UNCONFIRMED estimate
    total_due: Decimal | None  # None when cac_mode is UNCONFIRMED


def calculate_rsi(
    gross_revenue: Decimal,
    rate_rsi: Decimal,
    cac_mode: str,
    cac_rate: Decimal,
) -> TaxResult:
    """
    Calculate RSI Acompte for a given gross revenue.
    All arithmetic uses Decimal with ROUND_HALF_UP to 2 decimal places.
    Never uses float -- Decimal preserves exact XAF amounts.
    """
    base_acompte = (gross_revenue * rate_rsi).quantize(_TWO_PLACES, rounding=ROUND_HALF_UP)

    cac_amount: Decimal | None
    total_due: Decimal | None

    if cac_mode == "ADDITIVE":
        cac_amount = (base_acompte * cac_rate).quantize(_TWO_PLACES, rounding=ROUND_HALF_UP)
        total_due = base_acompte + cac_amount
    elif cac_mode == "INCLUDED":
        cac_amount = Decimal("0.00")
        total_due = base_acompte
    else:  # UNCONFIRMED -- Gate G1 not yet closed
        cac_amount = None
        total_due = None

    return TaxResult(
        gross_revenue=gross_revenue,
        base_acompte=base_acompte,
        cac_amount=cac_amount,
        cac_mode=cac_mode,
        cac_rate=cac_rate,
        total_due=total_due,
    )


# ── Formatting ───────────────────────────────────────────────────────────────


def _fmt_xaf(amount: Decimal) -> str:
    """Format a Decimal as an integer XAF amount with space thousands separators."""
    whole = int(amount.to_integral_value(rounding=ROUND_HALF_UP))
    return f"{abs(whole):,}".replace(",", " ")


_LABELS: Final[dict[str, dict[str, str]]] = {
    "fr": {
        "header": "*Calcul RSI*",
        "revenue": "Chiffre d'affaires",
        "acompte": "Acompte RSI (5,5 %)",
        "acompte_incl": "Acompte RSI (5,5 %, CAC inclus)",
        "cac_add": "CAC ({pct} %)",
        "cac_unc": "CAC (non confirme, estimation)",
        "total": "Total du",
        "sep": "-" * 28,
        "disclaimer": "Consultez votre comptable pour le montant CAC exact.",
    },
    "en": {
        "header": "*RSI Tax Calculation*",
        "revenue": "Revenue",
        "acompte": "RSI acompte (5.5%)",
        "acompte_incl": "RSI acompte (5.5%, CAC included)",
        "cac_add": "CAC ({pct}%)",
        "cac_unc": "CAC (unconfirmed, estimate)",
        "total": "Total due",
        "sep": "-" * 28,
        "disclaimer": "Please check with your accountant for the exact CAC amount.",
    },
    "pcm": {
        "header": "*RSI Tax*",
        "revenue": "Money wey yu make",
        "acompte": "RSI tax (5.5%)",
        "acompte_incl": "RSI tax (5.5%, CAC don include)",
        "cac_add": "CAC charge ({pct}%)",
        "cac_unc": "CAC (no confirm yet, na estimate)",
        "total": "Total wey yu go pay",
        "sep": "-" * 28,
        "disclaimer": "Abeg ask your accountant for di exact CAC amount.",
    },
}


def format_tax_result(result: TaxResult, language: str) -> str:
    """
    Format a TaxResult as a WhatsApp-ready message string.
    language: "fr" | "en" | "pcm" -- unknown codes fall back to French.
    Handles UNCONFIRMED mode by showing base_acompte as confirmed and
    CAC as a clearly labelled unconfirmed estimate (FR-TAX-2, Gate G1).
    """
    t = _LABELS.get(language, _LABELS["fr"])
    rev = _fmt_xaf(result.gross_revenue)
    base = _fmt_xaf(result.base_acompte)
    cac_pct = int(result.cac_rate * 100)

    lines: list[str] = [t["header"]]
    lines.append(f"{t['revenue']} : {rev} XAF")

    if result.cac_mode == "ADDITIVE":
        lines.append(f"{t['acompte']} : {base} XAF")
        lines.append(
            f"{t['cac_add'].format(pct=cac_pct)} : {_fmt_xaf(cast(Decimal, result.cac_amount))} XAF"
        )
        lines.append(t["sep"])
        lines.append(f"*{t['total']} : {_fmt_xaf(cast(Decimal, result.total_due))} XAF*")

    elif result.cac_mode == "INCLUDED":
        lines.append(f"{t['acompte_incl']} : {base} XAF")
        lines.append(t["sep"])
        lines.append(f"*{t['total']} : {_fmt_xaf(cast(Decimal, result.total_due))} XAF*")

    else:  # UNCONFIRMED
        cac_est = (result.base_acompte * result.cac_rate).quantize(
            _TWO_PLACES, rounding=ROUND_HALF_UP
        )
        lines.append(f"{t['acompte']} : {base} XAF ✓")
        lines.append(f"{t['cac_unc']} : ~{_fmt_xaf(cac_est)} XAF ⚠️")
        lines.append("")
        lines.append(f"⚠️ {t['disclaimer']}")

    return "\n".join(lines)
