"""add unique index on payment_transactions.campay_reference

Revision ID: b7e2d9f1a4c6
Revises: a3f1c8e2b5d9
Create Date: 2026-06-18

Prevents double-processing of duplicate Campay callbacks (SDD §4, Milestone 5).
NULL values are not considered equal in PostgreSQL UNIQUE indexes, so multiple
PENDING rows with campay_reference=NULL are allowed (transaction created before
Campay responds with a reference).
"""

from alembic import op


def upgrade() -> None:
    op.create_index(
        "ix_payment_transactions_campay_reference",
        "payment_transactions",
        ["campay_reference"],
        unique=True,
        postgresql_where="campay_reference IS NOT NULL",
    )


def downgrade() -> None:
    op.drop_index(
        "ix_payment_transactions_campay_reference",
        table_name="payment_transactions",
    )
