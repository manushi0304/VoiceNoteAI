from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.models.reminder import NotificationType, Reminder
from app.models.user import User
from app.services.email_service import EmailService
from app.services.websocket_manager import ws_manager


def _notification_value(reminder: Reminder) -> str:
    nt = reminder.notification_type
    if hasattr(nt, "value"):
        return nt.value
    return str(nt)


class ReminderSchedulerService:

    @staticmethod
    async def process_due_reminders():
        now = datetime.now(timezone.utc)

        async with AsyncSessionLocal() as session:  # type: AsyncSession
            result = await session.execute(
                select(Reminder).where(
                    Reminder.is_sent == False,
                    Reminder.reminder_time <= now,
                )
            )

            reminders = result.scalars().all()

            for reminder in reminders:
                when = reminder.reminder_time
                if when.tzinfo is None:
                    when = when.replace(tzinfo=timezone.utc)

                when_label = when.astimezone().strftime("%a, %b %d · %I:%M %p %Z")
                nt = _notification_value(reminder)
                send_push = nt in (NotificationType.push.value, NotificationType.both.value)
                send_email = nt in (NotificationType.email.value, NotificationType.both.value)

                print(
                    f"REMINDER TRIGGERED | user={reminder.user_id} | "
                    f"time={when.isoformat()} | notify={nt}"
                )

                if send_push:
                    await ws_manager.send_message(
                        str(reminder.user_id),
                        {
                            "type": "reminder",
                            "message": "Your scheduled reminder is due.",
                            "time": when.isoformat(),
                            "reminder_id": str(reminder.id),
                        },
                    )

                if send_email:
                    user = await session.get(User, reminder.user_id)
                    if user and user.email:
                        await EmailService.send_reminder_email(
                            to_email=user.email,
                            user_name=user.full_name,
                            reminder_time_display=when_label,
                            reminder_id=str(reminder.id),
                        )

                reminder.is_sent = True

            if reminders:
                await session.commit()
