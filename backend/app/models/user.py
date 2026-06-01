from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from app.models.base import Base, UUIDPrimaryKeyMixin, TimestampMixin


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    full_name: Mapped[str | None] = mapped_column(
        String(255)
    )

    preferred_language: Mapped[str] = mapped_column(
        String(10),
        default="en"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    # Relationships
    notes = relationship("Note", back_populates="user", cascade="all, delete")
    todos = relationship("Todo", back_populates="user", cascade="all, delete")
    reminders = relationship("Reminder", back_populates="user", cascade="all, delete")
