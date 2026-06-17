"""SQLAlchemy 2.0 ORM models for Tassi.

Table overview:
  users               — one row per WhatsApp user; no is_plus column (see property below)
  tax_calculations    — append-only; never UPDATE or DELETE rows (FR-DATA-1)
  subscriptions       — one row per subscription period; status transitions to EXPIRED on renewal
  payment_transactions — append-only; every Campay attempt is a new row (FR-DATA-1)
"""

import uuid
from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tassi.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # MSISDN in E.164 format: +237XXXXXXXXX
    whatsapp_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    # "fr" or "en" — set at onboarding (FR-CHAT-4)
    language: Mapped[str] = mapped_column(String(2), nullable=False, default="fr")
    # UNDER_10M | RSI_10_50M | OVER_50M | UNKNOWN — set at onboarding (FR-TAX-5)
    annual_revenue_band: Mapped[str | None] = mapped_column(String(16), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships — lazy="raise" forces callers to use selectinload() explicitly.
    # This prevents accidental N+1 queries in async code where lazy loading is unavailable.
    subscriptions: Mapped[list["Subscription"]] = relationship(
        "Subscription", back_populates="user", lazy="raise"
    )
    tax_calculations: Mapped[list["TaxCalculation"]] = relationship(
        "TaxCalculation", back_populates="user", lazy="raise"
    )
    payment_transactions: Mapped[list["PaymentTransaction"]] = relationship(
        "PaymentTransaction", back_populates="user", lazy="raise"
    )

    @property
    def is_plus(self) -> bool:
        """
        True if the user holds an ACTIVE subscription whose period_end is in the future.

        Stored as a computed property — not as a DB column — to avoid the data integrity
        risk of users.is_plus getting out of sync with the subscriptions table (APP.md §4.2).

        Callers loading this from the database MUST eager-load User.subscriptions first:
            selectinload(User.subscriptions)
        On transient (un-persisted) objects, subscriptions is an empty list → returns False.
        """
        now = datetime.now(tz=UTC)
        return any(s.status == "ACTIVE" and s.period_end > now for s in self.subscriptions)

    def __repr__(self) -> str:
        return f"<User id={self.id} whatsapp_id={self.whatsapp_id!r}>"


class TaxCalculation(Base):
    """
    Append-only record of every RSI Acompte calculation performed by Tassi.

    IMPORTANT: Never issue UPDATE or DELETE on this table. Each filing cycle
    creates a new row. The full history of rows IS the audit trail (FR-DATA-1).
    If a calculation is revised (e.g., after G1 closes), insert a corrected row
    and mark it with a note — do not overwrite the original.
    """

    __tablename__ = "tax_calculations"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    fiscal_period: Mapped[str] = mapped_column(String(7), nullable=False)  # "YYYY-MM"
    gross_revenue: Mapped[Decimal] = mapped_column(Numeric(precision=15, scale=2), nullable=False)
    base_acompte: Mapped[Decimal] = mapped_column(Numeric(precision=15, scale=2), nullable=False)
    # NULL when cac_mode is UNCONFIRMED (Gate G1 still open)
    cac_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=15, scale=2), nullable=True
    )
    # Records which CAC rule was active at calculation time.
    # Stored so records can be audited/corrected if G1 changes the answer.
    # Values: "ADDITIVE" | "INCLUDED" | "UNCONFIRMED"
    cac_mode: Mapped[str] = mapped_column(String(12), nullable=False)
    is_zero_return: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="tax_calculations", lazy="raise")

    __table_args__ = (
        # Composite index for the most common query pattern:
        # "fetch all calculations for user X in fiscal period Y"
        Index("ix_tax_calculations_user_period", "user_id", "fiscal_period"),
    )

    def __repr__(self) -> str:
        return (
            f"<TaxCalculation id={self.id} user_id={self.user_id}"
            f" period={self.fiscal_period!r}>"
        )


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    # "ACTIVE" | "EXPIRED" | "CANCELLED"
    status: Mapped[str] = mapped_column(String(12), nullable=False)
    period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    # Price paid in XAF (integer — XAF has no subunit coins in circulation)
    price_xaf: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="subscriptions", lazy="raise")
    payment_transactions: Mapped[list["PaymentTransaction"]] = relationship(
        "PaymentTransaction", back_populates="subscription", lazy="raise"
    )

    def __repr__(self) -> str:
        return f"<Subscription id={self.id} user_id={self.user_id} status={self.status!r}>"


class PaymentTransaction(Base):
    """
    Append-only record of every Campay payment attempt (FR-DATA-1).
    Never UPDATE status directly — Campay webhook or STATUS poll creates
    the transition by setting status on this row, but the row itself is
    the authoritative record of what happened.
    """

    __tablename__ = "payment_transactions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    # Nullable until the subscription is activated (transaction is created first)
    subscription_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("subscriptions.id"), nullable=True
    )
    # Campay's own reference — NULL until Campay responds to the push request
    campay_reference: Mapped[str | None] = mapped_column(String(128), nullable=True)
    # "MTN" | "ORANGE"
    operator: Mapped[str] = mapped_column(String(6), nullable=False)
    # Amount in XAF (integer)
    amount_xaf: Mapped[int] = mapped_column(nullable=False)
    # "PENDING" | "SUCCESS" | "FAILED"
    status: Mapped[str] = mapped_column(String(8), nullable=False, default="PENDING")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="payment_transactions", lazy="raise")
    subscription: Mapped["Subscription | None"] = relationship(
        "Subscription", back_populates="payment_transactions", lazy="raise"
    )

    def __repr__(self) -> str:
        return f"<PaymentTransaction id={self.id} status={self.status!r}>"
