from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.reminder import Reminder
from app.schemas.reminder import ReminderCreate
from app.utils.datetime_utils import normalize_to_utc


class ReminderService:

    @staticmethod
    def _serialize(reminder: Reminder) -> dict:
        return {
            "id": str(reminder.id),
            "reminder_time": reminder.reminder_time.isoformat(),
            "is_sent": reminder.is_sent,
            "notification_type": reminder.notification_type.value
            if hasattr(reminder.notification_type, "value")
            else reminder.notification_type,
            "created_at": reminder.created_at.isoformat() if reminder.created_at else None,
            "todo_id": str(reminder.todo_id) if reminder.todo_id else None,
            "todo_title": reminder.todo.title if reminder.todo else None,
        }

    @staticmethod
    async def list(db: AsyncSession, user_id: str):
        result = await db.execute(
            select(Reminder)
            .options(selectinload(Reminder.todo))
            .where(Reminder.user_id == user_id)
            .order_by(Reminder.reminder_time.asc())
        )
        reminders = result.scalars().all()
        now = datetime.now(timezone.utc)

        upcoming = []
        past = []
        for r in reminders:
            item = ReminderService._serialize(r)
            rt = r.reminder_time
            if rt.tzinfo is None:
                rt = rt.replace(tzinfo=timezone.utc)
            if r.is_sent or rt <= now:
                past.append(item)
            else:
                upcoming.append(item)

        past.sort(key=lambda x: x["reminder_time"], reverse=True)
        return upcoming + past

    @staticmethod
    async def create(db: AsyncSession, user_id: str, data: ReminderCreate):
        reminder_time = normalize_to_utc(data.reminder_time)

        todo_id = data.todo_id
        if not todo_id and data.todo_title:
            from app.services.todo_service import TodoService
            from app.schemas.todo import TodoCreate
            todo = await TodoService.create(
                db,
                user_id,
                TodoCreate(title=data.todo_title, priority="MEDIUM")
            )
            todo_id = todo.id

        reminder = Reminder(
            id=uuid4(),
            user_id=user_id,
            todo_id=todo_id,
            reminder_time=reminder_time,
            notification_type=data.notification_type,
            is_sent=False,
        )

        db.add(reminder)
        await db.commit()
        await db.refresh(reminder)

        if reminder.todo_id:
            from app.models.todo import Todo
            reminder.todo = await db.get(Todo, reminder.todo_id)

        return ReminderService._serialize(reminder)
