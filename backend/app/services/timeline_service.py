from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any

from app.models.note import Note
from app.models.todo import Todo, TodoStatus
from app.models.reminder import Reminder


class TimelineService:
    @staticmethod
    async def get_timeline(
        db: AsyncSession,
        user_id: str,
    ) -> List[Dict[str, Any]]:
        timeline: List[Dict[str, Any]] = []

        # -------------------------
        # NOTES
        # -------------------------
        notes_result = await db.execute(
            select(Note).where(Note.user_id == user_id)
        )
        for n in notes_result.scalars():
            timeline.append({
                "id": str(n.id),
                "type": "note",
                "text": n.content,
                "extra": {
                    "language": n.original_language,
                    "confidence": n.classification_confidence,
                },
                "created_at": n.created_at.isoformat(),
            })

        # -------------------------
        # TODOS
        # -------------------------
        todos_result = await db.execute(
            select(Todo).where(Todo.user_id == user_id)
        )
        for t in todos_result.scalars():
            timeline.append({
                "id": str(t.id),
                "type": "todo",
                "text": t.title,
                "extra": {
                    "priority": t.priority.value,
                    "status": t.status.value,
                    "completed": t.status == TodoStatus.COMPLETED,
                    "due_date": t.due_date.isoformat() if t.due_date else None,
                },
                "created_at": t.created_at.isoformat(),
            })

        # -------------------------
        # REMINDERS
        # -------------------------
        reminders_result = await db.execute(
            select(Reminder).where(Reminder.user_id == user_id)
        )
        for r in reminders_result.scalars():
            timeline.append({
                "id": str(r.id),
                "type": "reminder",
                "text": "Reminder",
                "extra": {
                    "reminder_time": r.reminder_time.isoformat(),
                    "notification_type": r.notification_type,
                    "is_sent": r.is_sent,
                },
                "created_at": r.created_at.isoformat(),
            })

        # -------------------------
        # SORT BY TIME (LATEST FIRST)
        # -------------------------
        timeline.sort(
            key=lambda x: x["created_at"],
            reverse=True
        )

        return timeline
