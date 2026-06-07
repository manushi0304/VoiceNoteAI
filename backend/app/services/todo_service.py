from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo import Todo
from app.schemas.todo import TodoCreate


class TodoService:

    # =====================================================
    # LIST TODOS
    # =====================================================
    @staticmethod
    async def list(
        db: AsyncSession,
        user_id: str
    ):
        from sqlalchemy import not_
        from app.models.reminder import Reminder

        # Exclude todos that have reminders associated with them
        reminder_todo_ids = select(Reminder.todo_id).where(Reminder.todo_id.isnot(None))

        result = await db.execute(
            select(Todo).where(
                Todo.user_id == user_id,
                not_(Todo.id.in_(reminder_todo_ids))
            )
        )

        todos = result.scalars().all()

        return [
            {
                "id": str(t.id),
                "title": t.title,
                "description": t.description,
                "priority": (
                    t.priority.value
                    if t.priority else None
                ),
                "status": (
                    t.status.value
                    if t.status else None
                ),
                "created_at": (
                    t.created_at.isoformat()
                    if t.created_at else None
                ),
                "completed_at": (
                    t.completed_at.isoformat()
                    if t.completed_at else None
                ),
            }
            for t in todos
        ]

    # =====================================================
    # CREATE TODO
    # =====================================================
    @staticmethod
    async def create(
        db: AsyncSession,
        user_id: str,
        data: TodoCreate
    ):

        todo = Todo(

            user_id=user_id,

            title=data.title,

            description=getattr(
                data,
                "description",
                None
            ),

            priority=getattr(
                data,
                "priority",
                "MEDIUM"
            ),
        )

        db.add(todo)

        await db.commit()

        await db.refresh(todo)

        return todo