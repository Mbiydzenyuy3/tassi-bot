"""Daily reminder jobs for Tassi (FR-NOTIF-1, FR-NOTIF-2, FR-NOTIF-3, FR-PAY-5)."""

import logging
from collections.abc import Callable, Coroutine
from datetime import UTC, datetime, timedelta

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tassi.config import Settings
from tassi.meta import send_text_message
from tassi.models import ReminderSent, Subscription, TaxCalculation, User

_log = logging.getLogger(__name__)

_MSG_DAY_14 = (
    "Rappel Tassi : la fenêtre de déclaration ferme demain. "
    "Envoyez votre calcul d'Acompte maintenant."
)
_MSG_DAY_10 = (
    "Rappel anticipé Tassi Plus : il reste 10 jours dans la fenêtre de déclaration. "
    "Pensez à enregistrer votre chiffre du mois."
)
_MSG_RENEWAL = (
    "Votre abonnement Tassi Plus expire dans 3 jours. "
    "Répondez RENOUVELER pour continuer à bénéficier des rappels anticipés."
)


async def send_day_14_reminders(fiscal_period: str, db: AsyncSession, cfg: Settings) -> int:
    """
    Query all users who have at least one tax_calculation in fiscal_period
    AND have not already been sent a Day-14 reminder for this period.
    Send the reminder via Meta API. Return count of messages sent.
    FR-NOTIF-1. Idempotent: calling twice on the same period sends zero the second time.
    """
    stmt = (
        select(User)
        .join(TaxCalculation, TaxCalculation.user_id == User.id)
        .where(TaxCalculation.fiscal_period == fiscal_period)
        .where(
            ~exists(
                select(ReminderSent.id).where(
                    ReminderSent.user_id == User.id,
                    ReminderSent.reminder_type == "day_14",
                    ReminderSent.fiscal_period == fiscal_period,
                )
            )
        )
        .distinct()
    )
    result = await db.execute(stmt)
    users = list(result.scalars().all())

    for user in users:
        await send_text_message(
            cfg.meta_phone_number_id,
            cfg.meta_access_token,
            user.whatsapp_id,
            _MSG_DAY_14,
        )
        db.add(
            ReminderSent(
                user_id=user.id,
                reminder_type="day_14",
                fiscal_period=fiscal_period,
            )
        )

    if users:
        await db.commit()
    return len(users)


async def send_day_10_reminders(fiscal_period: str, db: AsyncSession, cfg: Settings) -> int:
    """
    Query Plus subscribers (ACTIVE subscription) who have not been sent a Day-10 reminder
    for this period. Feature-flagged: returns 0 immediately when cfg.feature_plus_reminders
    is False. FR-NOTIF-2.
    """
    if not cfg.feature_plus_reminders:
        return 0

    stmt = (
        select(User)
        .join(Subscription, Subscription.user_id == User.id)
        .where(Subscription.status == "ACTIVE")
        .where(
            ~exists(
                select(ReminderSent.id).where(
                    ReminderSent.user_id == User.id,
                    ReminderSent.reminder_type == "day_10",
                    ReminderSent.fiscal_period == fiscal_period,
                )
            )
        )
        .distinct()
    )
    result = await db.execute(stmt)
    users = list(result.scalars().all())

    for user in users:
        await send_text_message(
            cfg.meta_phone_number_id,
            cfg.meta_access_token,
            user.whatsapp_id,
            _MSG_DAY_10,
        )
        db.add(
            ReminderSent(
                user_id=user.id,
                reminder_type="day_10",
                fiscal_period=fiscal_period,
            )
        )

    if users:
        await db.commit()
    return len(users)


async def send_renewal_prompts(db: AsyncSession, cfg: Settings) -> int:
    """
    Query all subscriptions with period_end between now() and now()+3 days and status=ACTIVE.
    Send renewal prompt. Idempotent per subscription (subscription_id key in reminders_sent).
    FR-PAY-5.
    """
    now = datetime.now(tz=UTC)
    window_end = now + timedelta(days=3)

    stmt = (
        select(Subscription, User)
        .join(User, User.id == Subscription.user_id)
        .where(Subscription.status == "ACTIVE")
        .where(Subscription.period_end >= now)
        .where(Subscription.period_end <= window_end)
        .where(
            ~exists(
                select(ReminderSent.id).where(
                    ReminderSent.subscription_id == Subscription.id,
                    ReminderSent.reminder_type == "renewal",
                )
            )
        )
    )
    result = await db.execute(stmt)
    rows = list(result.all())

    for sub, user in rows:
        await send_text_message(
            cfg.meta_phone_number_id,
            cfg.meta_access_token,
            user.whatsapp_id,
            _MSG_RENEWAL,
        )
        db.add(
            ReminderSent(
                user_id=user.id,
                subscription_id=sub.id,
                reminder_type="renewal",
                fiscal_period=None,
            )
        )

    if rows:
        await db.commit()
    return len(rows)


def make_daily_reminder_job(
    db_factory: async_sessionmaker[AsyncSession],
    cfg: Settings,
) -> Callable[[], Coroutine[None, None, None]]:
    """
    Return the async daily_reminder_job closure bound to db_factory and cfg.
    Used by APScheduler — the returned coroutine function takes no arguments.
    """

    async def daily_reminder_job() -> None:
        """
        Runs at 03:00 every day. Determines fiscal_period from today's date.
        Calls send_day_14_reminders on day 14, send_day_10_reminders on day 10,
        and send_renewal_prompts every day.
        Wraps everything in try/except — a failure must never crash the scheduler.
        FR-NOTIF-3.
        """
        try:
            today = datetime.now(tz=UTC)
            fiscal_period = today.strftime("%Y-%m")
            async with db_factory() as db:
                if today.day == 14:
                    await send_day_14_reminders(fiscal_period, db, cfg)
                if today.day == 10:
                    await send_day_10_reminders(fiscal_period, db, cfg)
                await send_renewal_prompts(db, cfg)
        except Exception:
            _log.exception("daily_reminder_job failed")

    return daily_reminder_job
