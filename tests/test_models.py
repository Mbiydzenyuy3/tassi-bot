"""Tests for tassi/models.py — model structure, types, and is_plus property."""

import uuid
from datetime import UTC, datetime
from decimal import Decimal

from tassi.models import PaymentTransaction, Subscription, TaxCalculation, User

# ── Helpers ───────────────────────────────────────────────────────────────────

_FAR_FUTURE = datetime(2099, 1, 1, tzinfo=UTC)
_FAR_PAST = datetime(2000, 1, 1, tzinfo=UTC)


def _make_user() -> User:
    return User(whatsapp_id="+237600000001")


def _make_subscription(*, status: str, period_end: datetime) -> Subscription:
    return Subscription(
        user_id=uuid.uuid4(),
        status=status,
        period_start=datetime(2026, 1, 1, tzinfo=UTC),
        period_end=period_end,
        price_xaf=500,
    )


# ── User ─────────────────────────────────────────────────────────────────────


class TestUser:
    def test_repr_contains_whatsapp_id(self) -> None:
        user = _make_user()
        assert "+237600000001" in repr(user)

    def test_repr_contains_class_name(self) -> None:
        user = _make_user()
        assert "User" in repr(user)

    def test_language_column_default_is_french(self) -> None:
        # mapped_column(default=...) is an INSERT-level default, not an __init__ default.
        # We verify the column definition rather than the instantiated object.
        col = User.__table__.c.language
        assert col.default is not None
        assert col.default.arg == "fr"

    def test_language_column_accepts_pcm(self) -> None:
        # "pcm" (3 chars) is the code for Cameroonian Pidgin English — column must be String(3)
        col = User.__table__.c.language
        assert col.type.length >= 3  # type: ignore[union-attr]

    def test_language_column_valid_values(self) -> None:
        for lang in ("fr", "en", "pcm"):
            user = User(whatsapp_id="+237600000099", language=lang)
            assert user.language == lang

    def test_annual_revenue_band_defaults_to_none(self) -> None:
        user = _make_user()
        assert user.annual_revenue_band is None

    def test_id_column_type_is_uuid(self) -> None:
        # Pass an explicit UUID so we can verify the column accepts the type.
        user = User(id=uuid.uuid4(), whatsapp_id="+237600000002")
        assert isinstance(user.id, uuid.UUID)

    def test_id_column_default_is_uuid4(self) -> None:
        # The column default must be uuid.uuid4 — SQLAlchemy calls it at INSERT time.
        col = User.__table__.c.id
        assert col.default is not None
        assert col.default.arg.__name__ == "uuid4"
        assert col.default.arg.__module__ == "uuid"


# ── User.is_plus property ─────────────────────────────────────────────────────


class TestUserIsPlus:
    def test_false_when_no_subscriptions(self) -> None:
        user = _make_user()
        # transient object: subscriptions initialises as an empty list
        assert user.is_plus is False

    def test_false_when_subscription_is_expired_status(self) -> None:
        user = _make_user()
        sub = _make_subscription(status="EXPIRED", period_end=_FAR_FUTURE)
        user.subscriptions = [sub]
        assert user.is_plus is False

    def test_false_when_subscription_is_cancelled(self) -> None:
        user = _make_user()
        sub = _make_subscription(status="CANCELLED", period_end=_FAR_FUTURE)
        user.subscriptions = [sub]
        assert user.is_plus is False

    def test_false_when_active_but_period_end_in_past(self) -> None:
        user = _make_user()
        sub = _make_subscription(status="ACTIVE", period_end=_FAR_PAST)
        user.subscriptions = [sub]
        assert user.is_plus is False

    def test_true_when_active_subscription_with_future_period_end(self) -> None:
        user = _make_user()
        sub = _make_subscription(status="ACTIVE", period_end=_FAR_FUTURE)
        user.subscriptions = [sub]
        assert user.is_plus is True

    def test_true_when_one_active_among_multiple_subscriptions(self) -> None:
        user = _make_user()
        expired = _make_subscription(status="EXPIRED", period_end=_FAR_PAST)
        active = _make_subscription(status="ACTIVE", period_end=_FAR_FUTURE)
        user.subscriptions = [expired, active]
        assert user.is_plus is True

    def test_false_when_all_subscriptions_are_expired(self) -> None:
        user = _make_user()
        s1 = _make_subscription(status="EXPIRED", period_end=_FAR_PAST)
        s2 = _make_subscription(status="EXPIRED", period_end=_FAR_PAST)
        user.subscriptions = [s1, s2]
        assert user.is_plus is False


# ── TaxCalculation ────────────────────────────────────────────────────────────


class TestTaxCalculation:
    def test_repr_contains_fiscal_period(self) -> None:
        calc = TaxCalculation(
            user_id=uuid.uuid4(),
            fiscal_period="2026-06",
            gross_revenue=Decimal("2350000.00"),
            base_acompte=Decimal("129250.00"),
            cac_mode="UNCONFIRMED",
        )
        assert "2026-06" in repr(calc)

    def test_gross_revenue_accepts_decimal(self) -> None:
        calc = TaxCalculation(
            user_id=uuid.uuid4(),
            fiscal_period="2026-06",
            gross_revenue=Decimal("2350000.00"),
            base_acompte=Decimal("129250.00"),
            cac_mode="UNCONFIRMED",
        )
        assert calc.gross_revenue == Decimal("2350000.00")

    def test_gross_revenue_is_not_float(self) -> None:
        calc = TaxCalculation(
            user_id=uuid.uuid4(),
            fiscal_period="2026-06",
            gross_revenue=Decimal("1500000.00"),
            base_acompte=Decimal("82500.00"),
            cac_mode="ADDITIVE",
        )
        assert not isinstance(calc.gross_revenue, float)

    def test_cac_amount_nullable_for_unconfirmed(self) -> None:
        calc = TaxCalculation(
            user_id=uuid.uuid4(),
            fiscal_period="2026-06",
            gross_revenue=Decimal("2350000.00"),
            base_acompte=Decimal("129250.00"),
            cac_amount=None,
            cac_mode="UNCONFIRMED",
        )
        assert calc.cac_amount is None

    def test_is_zero_return_column_default_is_false(self) -> None:
        col = TaxCalculation.__table__.c.is_zero_return
        assert col.default is not None
        assert col.default.arg is False

    def test_cac_mode_values(self) -> None:
        for mode in ("ADDITIVE", "INCLUDED", "UNCONFIRMED"):
            calc = TaxCalculation(
                user_id=uuid.uuid4(),
                fiscal_period="2026-06",
                gross_revenue=Decimal("1000000.00"),
                base_acompte=Decimal("55000.00"),
                cac_mode=mode,
            )
            assert calc.cac_mode == mode

    def test_has_composite_index(self) -> None:
        index_names = {idx.name for idx in TaxCalculation.__table__.indexes}
        assert "ix_tax_calculations_user_period" in index_names


# ── Subscription ──────────────────────────────────────────────────────────────


class TestSubscription:
    def test_repr_contains_status(self) -> None:
        sub = _make_subscription(status="ACTIVE", period_end=_FAR_FUTURE)
        assert "ACTIVE" in repr(sub)

    def test_status_values(self) -> None:
        for status in ("ACTIVE", "EXPIRED", "CANCELLED"):
            sub = _make_subscription(status=status, period_end=_FAR_FUTURE)
            assert sub.status == status

    def test_price_xaf_is_integer(self) -> None:
        sub = _make_subscription(status="ACTIVE", period_end=_FAR_FUTURE)
        assert isinstance(sub.price_xaf, int)


# ── PaymentTransaction ────────────────────────────────────────────────────────


class TestPaymentTransaction:
    def test_repr_contains_status(self) -> None:
        pt = PaymentTransaction(
            user_id=uuid.uuid4(),
            operator="MTN",
            amount_xaf=500,
            status="PENDING",
        )
        assert "PENDING" in repr(pt)

    def test_status_values(self) -> None:
        for status in ("PENDING", "SUCCESS", "FAILED"):
            pt = PaymentTransaction(
                user_id=uuid.uuid4(),
                operator="MTN",
                amount_xaf=500,
                status=status,
            )
            assert pt.status == status

    def test_operator_values(self) -> None:
        for operator in ("MTN", "ORANGE"):
            pt = PaymentTransaction(
                user_id=uuid.uuid4(),
                operator=operator,
                amount_xaf=500,
                status="PENDING",
            )
            assert pt.operator == operator

    def test_status_column_default_is_pending(self) -> None:
        col = PaymentTransaction.__table__.c.status
        assert col.default is not None
        assert col.default.arg == "PENDING"

    def test_campay_reference_defaults_to_none(self) -> None:
        pt = PaymentTransaction(
            user_id=uuid.uuid4(),
            operator="MTN",
            amount_xaf=500,
            status="PENDING",
        )
        assert pt.campay_reference is None

    def test_subscription_id_is_nullable(self) -> None:
        pt = PaymentTransaction(
            user_id=uuid.uuid4(),
            operator="MTN",
            amount_xaf=500,
            status="PENDING",
        )
        assert pt.subscription_id is None

    def test_amount_xaf_is_integer(self) -> None:
        pt = PaymentTransaction(
            user_id=uuid.uuid4(),
            operator="MTN",
            amount_xaf=500,
            status="PENDING",
        )
        assert isinstance(pt.amount_xaf, int)
