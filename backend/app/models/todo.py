from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, Enum, DateTime
from app.models.base import Base, UUIDPrimaryKeyMixin, TimestampMixin
import enum


class Priority(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class TodoStatus(enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Todo(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "todos"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )

    note_id: Mapped[str | None] = mapped_column(
        ForeignKey("notes.id", ondelete="SET NULL")
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text
    )

    priority: Mapped[Priority] = mapped_column(
        Enum(Priority, name="priority_enum"),
        default=Priority.MEDIUM
    )

    status: Mapped[TodoStatus] = mapped_column(
        Enum(TodoStatus, name="todo_status_enum"),
        default=TodoStatus.PENDING,
        index=True
    )

    due_date: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True)
    )

    completed_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True)
    )

    user = relationship("User", back_populates="todos")
    note = relationship("Note")
