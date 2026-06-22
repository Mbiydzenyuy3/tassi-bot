"""add reminders_sent table

Revision ID: 0003
Revises: b7e2d9f1a4c6
Create Date: 2026-06-20
"""

import sqlalchemy as sa
from alembic import op

revision = "0003"
down_revision = "b7e2d9f1a4c6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "reminders_sent",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("user_id", sa.Uuid(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("reminder_type", sa.String(8), nullable=False),
        sa.Column("fiscal_period", sa.String(7), nullable=True),
        sa.Column(
            "subscription_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("subscriptions.id"),
            nullable=True,
        ),
        sa.Column(
            "sent_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index(
        "uq_reminders_sent_period",
        "reminders_sent",
        ["user_id", "reminder_type", "fiscal_period"],
        unique=True,
        postgresql_where=sa.text("fiscal_period IS NOT NULL"),
    )
    op.create_index(
        "uq_reminders_sent_renewal",
        "reminders_sent",
        ["subscription_id"],
        unique=True,
        postgresql_where=sa.text("subscription_id IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index("uq_reminders_sent_renewal", table_name="reminders_sent")
    op.drop_index("uq_reminders_sent_period", table_name="reminders_sent")
    op.drop_table("reminders_sent")
