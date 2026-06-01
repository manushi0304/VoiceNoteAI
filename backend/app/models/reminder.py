import enum
from sqlalchemy import Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.models.base import Base, UUIDPrimaryKeyMixin, TimestampMixin


class NotificationType(enum.Enum):
    """Matches DB enum: email, push (in-app), both."""

    email = "email"
    push = "push"
    both = "both"


class Reminder(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "reminders"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    todo_id: Mapped[str | None] = mapped_column(
        ForeignKey("todos.id", ondelete="SET NULL"),
        nullable=True,
    )

    reminder_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    notification_type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType, name="notification_type_enum"),
        default=NotificationType.both,
        nullable=False,
    )

    is_sent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    user = relationship("User", back_populates="reminders")
