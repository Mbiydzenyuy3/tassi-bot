"""
Campay payment callback processing (FR-PAY-3).

process_payment_callback is called from BackgroundTasks after the
/campay/webhook endpoint acks the request. It is fully idempotent:
a second call with the same campay_reference is a no-op.
"""

import logging
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tassi.config import Settings
from tassi.meta import send_text_message
from tassi.models import PaymentTransaction, Subscription, User
from tassi.templates import get_message

_log = logging.getLogger(__name__)


async def process_payment_callback(
    campay_reference: str,
    status: str,
    db: AsyncSession,
    cfg: Settings,
) -> None:
    """
    On SUCCESS: find PENDING PaymentTransaction, activate subscription, confirm to user.
    On FAILED: update to FAILED, notify user.
    Idempotent: already-processed transactions are silently skipped.
    FR-PAY-3.
    """
    async with db.begin():
        result = await db.execute(
            select(PaymentTransaction)
            .join(User)
            .where(PaymentTransaction.campay_reference == campay_reference)
            .limit(1)
        )
        tx = result.scalar_one_or_none()

        if tx is None:
            _log.warning("campay callback for unknown reference=%s", campay_reference)
            return

        if tx.status != "PENDING":
            _log.info("campay callback ignored — already processed reference=%s", campay_reference)
            return

        # Fetch msisdn for the WhatsApp reply
        user_result = await db.execute(select(User).where(User.id == tx.user_id))
        user = user_result.scalar_one()
        msisdn = user.whatsapp_id
        language = user.language

        if status == "SUCCESS":
            tx.status = "SUCCESS"
            tx.updated_at = datetime.now(tz=UTC)

            now = datetime.now(tz=UTC)
            sub = Subscription(
                user_id=tx.user_id,
                status="ACTIVE",
                period_start=now,
                period_end=now + timedelta(days=30),
                price_xaf=tx.amount_xaf,
            )
            db.add(sub)
            await db.flush()
            tx.subscription_id = sub.id

            msg_key = "payment_confirmed"
        else:
            tx.status = "FAILED"
            tx.updated_at = datetime.now(tz=UTC)
            msg_key = "payment_failed"

    text = get_message(language, msg_key)
    try:
        await send_text_message(cfg.meta_phone_number_id, cfg.meta_access_token, msisdn, text)
    except Exception:
        _log.exception("failed to send payment status message to %s", msisdn)
