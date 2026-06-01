from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Float, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from app.models.base import Base, UUIDPrimaryKeyMixin, TimestampMixin
import enum


class ContentType(enum.Enum):
    note = "note"
    todo = "todo"
    reminder = "reminder"


class Note(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "notes"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )

    title: Mapped[str | None] = mapped_column(
        String(255)
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    original_language: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    translated_content: Mapped[dict | None] = mapped_column(
        JSONB
    )

    content_type: Mapped[ContentType] = mapped_column(
        Enum(ContentType, name="content_type_enum"),
        index=True
    )

    classification_confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0
    )

    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(384)
    )

    audio_url: Mapped[str | None] = mapped_column(
        String(500)
    )

    user = relationship("User", back_populates="notes")
