"""initial schema

Revision ID: a3f1c8e2b5d9
Revises:
Create Date: 2026-06-17

Creates all four Tassi tables:
  users, subscriptions, tax_calculations, payment_transactions

Tables are created in FK-dependency order; downgrade drops in reverse order.
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "a3f1c8e2b5d9"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── 1. users ─────────────────────────────────────────────────────────────
    # No foreign key dependencies — create first.
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("whatsapp_id", sa.String(32), nullable=False),
        sa.Column("language", sa.String(3), nullable=False, server_default="fr"),
        sa.Column("annual_revenue_band", sa.String(16), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("whatsapp_id"),
    )

    # ── 2. subscriptions ──────────────────────────────────────────────────────
    # FK → users.id. Must exist before payment_transactions references it.
    op.create_table(
        "subscriptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(12), nullable=False),
        sa.Column("period_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("period_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("price_xaf", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # ── 3. tax_calculations ───────────────────────────────────────────────────
    # FK → users.id. Append-only — never UPDATE or DELETE rows (FR-DATA-1).
    op.create_table(
        "tax_calculations",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("fiscal_period", sa.String(7), nullable=False),
        sa.Column("gross_revenue", sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column("base_acompte", sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column("cac_amount", sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column("cac_mode", sa.String(12), nullable=False),
        sa.Column("is_zero_return", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_tax_calculations_user_period",
        "tax_calculations",
        ["user_id", "fiscal_period"],
    )

    # ── 4. payment_transactions ───────────────────────────────────────────────
    # FK → users.id AND subscriptions.id. Append-only (FR-DATA-1).
    op.create_table(
        "payment_transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("subscription_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("campay_reference", sa.String(128), nullable=True),
        sa.Column("operator", sa.String(6), nullable=False),
        sa.Column("amount_xaf", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(8), nullable=False, server_default=sa.text("'PENDING'")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["subscription_id"], ["subscriptions.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    # Drop in reverse FK-dependency order.
    op.drop_table("payment_transactions")
    op.drop_index("ix_tax_calculations_user_period", table_name="tax_calculations")
    op.drop_table("tax_calculations")
    op.drop_table("subscriptions")
    op.drop_table("users")
