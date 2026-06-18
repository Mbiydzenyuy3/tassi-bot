"""
Conversation state machine for Tassi (Milestone 4).

States stored in Redis session["state"]:
  NEW               — first contact, no session yet
  AWAITING_LANGUAGE — language picker sent
  AWAITING_BAND     — revenue band picker sent
  ACTIVE            — onboarding complete, ready for revenue input
"""

import logging
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload

from tassi.campay import get_transaction_status, initiate_ussd_push
from tassi.config import Settings
from tassi.meta import send_text_message
from tassi.models import PaymentTransaction, TaxCalculation, User
from tassi.payments import process_payment_callback
from tassi.session import get_session, set_session
from tassi.tax import (
    TaxResult,
    calculate_rsi,
    format_tax_result,
    is_zero_return,
    parse_revenue,
)
from tassi.templates import get_message

_log = logging.getLogger(__name__)

# ── State constants ──────────────────────────────────────────────────────────

_NEW = "NEW"
_AWAITING_LANGUAGE = "AWAITING_LANGUAGE"
_AWAITING_BAND = "AWAITING_BAND"
_ACTIVE = "ACTIVE"
_AWAITING_OPERATOR = "AWAITING_OPERATOR"

# Band selection input → all map to RSI_10_50M
_IN_BAND_CHOICES = frozenset({"1", "2", "3", "4"})

# RSI floor/ceiling for free-text revenue at band selection (FR-TAX-5)
_RSI_MIN = Decimal("10_000_000")
_RSI_MAX = Decimal("50_000_000")

# Max rejections before giving up on out-of-band user
_MAX_BAND_TRIES = 3

# RESEND trigger words (all languages)
_RESEND_WORDS = frozenset({"resend", "renvoyer", "send again", "send am again"})

# Payment command trigger words
_SUBSCRIBE_WORDS = frozenset({"subscribe", "abonnement"})
_STATUS_WORDS = frozenset({"status", "statut"})
_HISTORY_WORDS = frozenset({"history", "historique"})

# Operator selection in AWAITING_OPERATOR state
_OPERATOR_MTN = frozenset({"1", "mtn"})
_OPERATOR_ORANGE = frozenset({"2", "orange"})

# Minimum age before STATUS triggers a Campay poll (FR-PAY-4)
_STATUS_POLL_AFTER = timedelta(minutes=2)

# ── Language detection keyword sets ──────────────────────────────────────────
# Used when the user types free text instead of choosing 1/2/3.
# Scored by word overlap; highest score wins; defaults to "fr".

_FR_WORDS = frozenset(
    {
        "bonjour",
        "bonsoir",
        "salut",
        "merci",
        "oui",
        "non",
        "rien",
        "chiffre",
        "affaires",
        "frs",
        "vente",
        "revenu",
        "mois",
        "taxe",
        "impot",
        "declaration",
        "neant",
        "je",
        "vous",
        "nous",
        "mon",
        "ma",
        "pas",
        "avec",
        "pour",
        "est",
        "les",
        "des",
        "une",
        "voila",
    }
)

_EN_WORDS = frozenset(
    {
        "hello",
        "hi",
        "hey",
        "yes",
        "no",
        "thanks",
        "thank",
        "revenue",
        "sales",
        "profit",
        "income",
        "month",
        "tax",
        "declaration",
        "nothing",
        "good",
        "morning",
        "evening",
        "please",
        "help",
        "have",
        "my",
    }
)

# Pidgin phrases/words — checked as substrings because many are multi-word
_PCM_PHRASES = (
    "abeg",
    "na ",
    " na",
    "wey",
    " dey",
    "wahala",
    "sabi",
    "oga",
    "bros",
    "how far",
    "how now",
    "e no",
    "i no",
    "no be",
    "no money",
    "e finish",
    "nothing dey",
    "no sell",
    "i no sell",
)


def _detect_language(text: str) -> str:
    """
    Infer fr/en/pcm from free text when the user skips the language picker.
    Pidgin checked first (most distinctive vocabulary); then fr vs en by
    word-overlap score; falls back to "fr" (SRS FR-CHAT-4 default).
    """
    lower = text.lower()
    words = set(lower.split())

    pcm_score = sum(1 for phrase in _PCM_PHRASES if phrase in lower)
    fr_score = len(words & _FR_WORDS)
    en_score = len(words & _EN_WORDS)

    if pcm_score > 0 and pcm_score >= fr_score and pcm_score >= en_score:
        return "pcm"
    if fr_score >= en_score and fr_score > 0:
        return "fr"
    if en_score > 0:
        return "en"
    return "fr"


# ── Entry point ──────────────────────────────────────────────────────────────


async def handle_message(
    msisdn: str,
    message_text: str,
    _message_id: str,
    db_factory: async_sessionmaker[AsyncSession],
    redis: Redis,  # type: ignore[type-arg]
    cfg: Settings,
) -> None:
    """
    Main message handler dispatched from BackgroundTasks in the webhook route.
    Creates its own DB session — the request-scoped session is already closed
    by the time BackgroundTasks executes.
    """
    async with db_factory() as db:
        session = await get_session(redis, msisdn)
        state = str(session.get("state", _NEW))
        language = str(session.get("language", "fr"))

        if state == _NEW:
            await _handle_new(msisdn, redis, cfg)
        elif state == _AWAITING_LANGUAGE:
            await _handle_awaiting_language(msisdn, message_text, session, redis, cfg)
        elif state == _AWAITING_BAND:
            await _handle_awaiting_band(msisdn, message_text, session, redis, cfg)
        elif state == _ACTIVE:
            await _handle_active(msisdn, message_text, session, db, redis, cfg, language)
        elif state == _AWAITING_OPERATOR:
            await _handle_awaiting_operator(msisdn, message_text, session, db, redis, cfg, language)
        else:
            _log.warning("unknown state %r for msisdn=%s — resetting", state, msisdn)
            await set_session(redis, msisdn, {})
            await _handle_new(msisdn, redis, cfg)


# ── State handlers ────────────────────────────────────────────────────────────


async def _handle_new(
    msisdn: str,
    redis: Redis,  # type: ignore[type-arg]
    cfg: Settings,
) -> None:
    new_session: dict[str, object] = {"state": _AWAITING_LANGUAGE, "language": "fr"}
    await set_session(redis, msisdn, new_session)
    await _send(msisdn, "fr", "ask_language", cfg)


async def _handle_awaiting_language(
    msisdn: str,
    text: str,
    session: dict[str, object],
    redis: Redis,  # type: ignore[type-arg]
    cfg: Settings,
) -> None:
    normalized = text.strip().lower()
    if normalized in ("1", "fr", "français", "francais"):
        lang = "fr"
    elif normalized in ("2", "en", "english"):
        lang = "en"
    elif normalized in ("3", "pcm", "pidgin"):
        lang = "pcm"
    else:
        # User skipped the picker and typed free text — detect their language
        # from what they wrote rather than blocking them with a reprompt.
        lang = _detect_language(normalized)

    session["language"] = lang
    session["state"] = _AWAITING_BAND
    await set_session(redis, msisdn, session)
    await _send(msisdn, lang, "ask_revenue_band", cfg)


async def _handle_awaiting_band(
    msisdn: str,
    text: str,
    session: dict[str, object],
    redis: Redis,  # type: ignore[type-arg]
    cfg: Settings,
) -> None:
    lang = str(session.get("language", "fr"))
    normalized = text.strip()

    in_band = False
    if normalized in _IN_BAND_CHOICES:
        in_band = True
    else:
        revenue = parse_revenue(normalized)
        if revenue is not None and _RSI_MIN <= revenue <= _RSI_MAX:
            in_band = True

    if in_band:
        session["state"] = _ACTIVE
        session["annual_revenue_band"] = "RSI_10_50M"
        session.pop("band_tries", None)
        await set_session(redis, msisdn, session)
        await _send(msisdn, lang, "ask_revenue", cfg)
        return

    raw_tries = session.get("band_tries", 0)
    tries = (raw_tries if isinstance(raw_tries, int) else 0) + 1
    if tries >= _MAX_BAND_TRIES:
        session.pop("band_tries", None)
        await set_session(redis, msisdn, session)
        await _send(msisdn, lang, "out_of_band_final", cfg)
    else:
        session["band_tries"] = tries
        await set_session(redis, msisdn, session)
        await _send(msisdn, lang, "out_of_band", cfg)


async def _handle_active(
    msisdn: str,
    text: str,
    session: dict[str, object],
    db: AsyncSession,
    redis: Redis,  # type: ignore[type-arg]
    cfg: Settings,
    language: str,
) -> None:
    normalized = text.strip()
    lower = normalized.lower()

    # RESEND command
    if lower in _RESEND_WORDS:
        await _handle_resend(msisdn, db, cfg, language)
        return

    # SUBSCRIBE command (FR-SUB-1, FR-PAY-1)
    if lower in _SUBSCRIBE_WORDS:
        await _handle_subscribe(msisdn, session, db, redis, cfg, language)
        return

    # STATUS command (FR-PAY-4)
    if lower in _STATUS_WORDS:
        await _handle_status(msisdn, db, cfg, language)
        return

    # HISTORY command (FR-SUB-3)
    if lower in _HISTORY_WORDS:
        await _handle_history(msisdn, db, cfg, language)
        return

    # Zero-return path (FR-TAX-3)
    if is_zero_return(normalized):
        await _send(msisdn, language, "zero_return_guidance", cfg)
        fiscal_period = datetime.now(tz=UTC).strftime("%Y-%m")
        await _persist_zero_return(msisdn, fiscal_period, db)
        return

    # Revenue calculation path (FR-TAX-1/2/4)
    revenue = parse_revenue(normalized)
    if revenue is None:
        await _send(msisdn, language, "invalid_input", cfg)
        return

    rate_rsi = Decimal(cfg.rate_rsi)
    cac_rate = Decimal(cfg.cac_rate)
    result = calculate_rsi(revenue, rate_rsi, cfg.cac_mode, cac_rate)
    formatted = format_tax_result(result, language)

    fiscal_period = datetime.now(tz=UTC).strftime("%Y-%m")
    await _persist_calculation(msisdn, result, fiscal_period, db)
    await _send(msisdn, language, "calculation_result", cfg, tax_result=formatted)


async def _handle_subscribe(
    msisdn: str,
    session: dict[str, object],
    db: AsyncSession,
    redis: Redis,  # type: ignore[type-arg]
    cfg: Settings,
    language: str,
) -> None:
    result = await db.execute(
        select(User).options(selectinload(User.subscriptions)).where(User.whatsapp_id == msisdn)
    )
    user = result.scalar_one_or_none()
    if user and user.is_plus:
        await _send(msisdn, language, "already_subscribed", cfg)
        return

    session["state"] = _AWAITING_OPERATOR
    await set_session(redis, msisdn, session)
    await _send(msisdn, language, "ask_operator", cfg, price_xaf=str(cfg.plus_price_xaf))


async def _handle_awaiting_operator(
    msisdn: str,
    text: str,
    session: dict[str, object],
    db: AsyncSession,
    redis: Redis,  # type: ignore[type-arg]
    cfg: Settings,
    language: str,
) -> None:
    normalized = text.strip().lower()
    if normalized in _OPERATOR_MTN:
        operator = "MTN"
    elif normalized in _OPERATOR_ORANGE:
        operator = "ORANGE"
    else:
        await _send(msisdn, language, "ask_operator", cfg, price_xaf=str(cfg.plus_price_xaf))
        return

    session["state"] = _ACTIVE
    await set_session(redis, msisdn, session)

    user = await _get_or_create_user(msisdn, db)
    tx = PaymentTransaction(
        user_id=user.id,
        operator=operator,
        amount_xaf=cfg.plus_price_xaf,
        status="PENDING",
    )

    try:
        reference = await initiate_ussd_push(
            cfg.campay_username,
            cfg.campay_password,
            cfg.campay_application_token,
            cfg.plus_price_xaf,
            msisdn,
            "Tassi Plus subscription",
            str(tx.id),
        )
        tx.campay_reference = reference
    except Exception:
        _log.exception("campay push failed for msisdn=%s", msisdn)
        await _send(msisdn, language, "subscribe_error", cfg)
        return

    async with db.begin():
        db.add(tx)

    await _send(msisdn, language, "subscribe_initiated", cfg)


async def _handle_status(
    msisdn: str,
    db: AsyncSession,
    cfg: Settings,
    language: str,
) -> None:
    result = await db.execute(
        select(PaymentTransaction)
        .join(User)
        .where(
            User.whatsapp_id == msisdn,
            PaymentTransaction.status == "PENDING",
        )
        .order_by(PaymentTransaction.created_at.desc())
        .limit(1)
    )
    tx = result.scalar_one_or_none()

    if tx is None:
        await _send(msisdn, language, "no_pending_payment", cfg)
        return

    age = datetime.now(tz=UTC) - tx.created_at.replace(tzinfo=UTC)
    if age < _STATUS_POLL_AFTER:
        await _send(msisdn, language, "payment_just_initiated", cfg)
        return

    if tx.campay_reference is None:
        await _send(msisdn, language, "payment_pending", cfg)
        return

    polled = await get_transaction_status(cfg.campay_application_token, tx.campay_reference)
    if polled in {"SUCCESS", "FAILED"}:
        await process_payment_callback(tx.campay_reference, polled, db, cfg)
    else:
        await _send(msisdn, language, "payment_pending", cfg)


async def _handle_history(
    msisdn: str,
    db: AsyncSession,
    cfg: Settings,
    language: str,
) -> None:
    result = await db.execute(
        select(User).options(selectinload(User.subscriptions)).where(User.whatsapp_id == msisdn)
    )
    user = result.scalar_one_or_none()

    if not user or not user.is_plus:
        await _send(msisdn, language, "history_not_plus", cfg)
        return

    calcs_result = await db.execute(
        select(TaxCalculation)
        .where(
            TaxCalculation.user_id == user.id,
            TaxCalculation.is_zero_return == False,  # noqa: E712
        )
        .order_by(TaxCalculation.created_at.desc())
        .limit(12)
    )
    calcs = calcs_result.scalars().all()

    if not calcs:
        await _send(msisdn, language, "history_empty", cfg)
        return

    lines = [f"{c.fiscal_period}: {int(c.base_acompte):,} XAF".replace(",", " ") for c in calcs]
    history_text = "📋 *Historique RSI*\n\n" + "\n".join(lines)
    await _send(msisdn, language, "history_result", cfg, history_text=history_text)


# ── DB helpers ────────────────────────────────────────────────────────────────


async def _get_or_create_user(msisdn: str, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.whatsapp_id == msisdn))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(whatsapp_id=msisdn)
        db.add(user)
        await db.flush()
    return user


async def _persist_calculation(
    msisdn: str,
    result: TaxResult,
    fiscal_period: str,
    db: AsyncSession,
) -> None:
    async with db.begin():
        user = await _get_or_create_user(msisdn, db)
        calc = TaxCalculation(
            user_id=user.id,
            fiscal_period=fiscal_period,
            gross_revenue=result.gross_revenue,
            base_acompte=result.base_acompte,
            cac_amount=result.cac_amount,
            cac_mode=result.cac_mode,
            is_zero_return=False,
        )
        db.add(calc)


async def _persist_zero_return(
    msisdn: str,
    fiscal_period: str,
    db: AsyncSession,
) -> None:
    async with db.begin():
        user = await _get_or_create_user(msisdn, db)
        calc = TaxCalculation(
            user_id=user.id,
            fiscal_period=fiscal_period,
            gross_revenue=Decimal("0.00"),
            base_acompte=Decimal("0.00"),
            cac_amount=None,
            cac_mode="UNCONFIRMED",
            is_zero_return=True,
        )
        db.add(calc)


async def _handle_resend(
    msisdn: str,
    db: AsyncSession,
    cfg: Settings,
    language: str,
) -> None:
    fiscal_period = datetime.now(tz=UTC).strftime("%Y-%m")
    result = await db.execute(
        select(TaxCalculation)
        .join(User)
        .where(
            User.whatsapp_id == msisdn,
            TaxCalculation.fiscal_period == fiscal_period,
            TaxCalculation.is_zero_return == False,  # noqa: E712
        )
        .order_by(TaxCalculation.created_at.desc())
        .limit(1)
    )
    calc = result.scalar_one_or_none()
    if calc is None:
        await _send(msisdn, language, "resend_no_history", cfg)
        return

    rebuilt = TaxResult(
        gross_revenue=calc.gross_revenue,
        base_acompte=calc.base_acompte,
        cac_amount=calc.cac_amount,
        cac_mode=calc.cac_mode,
        cac_rate=Decimal(cfg.cac_rate),
        total_due=(
            calc.base_acompte + calc.cac_amount
            if calc.cac_mode == "ADDITIVE" and calc.cac_amount is not None
            else (calc.base_acompte if calc.cac_mode == "INCLUDED" else None)
        ),
    )
    formatted = format_tax_result(rebuilt, language)
    await _send(msisdn, language, "resend_result", cfg, tax_result=formatted)


# ── Send helper ───────────────────────────────────────────────────────────────


async def _send(
    msisdn: str,
    language: str,
    key: str,
    cfg: Settings,
    **kwargs: str,
) -> None:
    text = get_message(language, key, **kwargs)
    try:
        await send_text_message(cfg.meta_phone_number_id, cfg.meta_access_token, msisdn, text)
    except Exception:
        _log.exception("failed to send message key=%r to %s", key, msisdn)
