from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator

from app.utils.datetime_utils import normalize_to_utc


class NotificationType(str, Enum):
    email = "email"
    push = "push"
    both = "both"


class ReminderCreate(BaseModel):
    reminder_time: datetime
    notification_type: NotificationType = NotificationType.both
    todo_id: Optional[UUID] = None
    todo_title: Optional[str] = None

    @field_validator("reminder_time", mode="before")
    @classmethod
    def parse_time(cls, value):
        if isinstance(value, str):
            value = value.replace("Z", "+00:00")
            return datetime.fromisoformat(value)
        return value

    @field_validator("reminder_time", mode="after")
    @classmethod
    def ensure_future_utc(cls, value: datetime) -> datetime:
        utc = normalize_to_utc(value)
        now = datetime.now(timezone.utc)
        if utc <= now - timedelta(seconds=30):
            raise ValueError("Reminder time must be in the future")
        return utc


class ReminderResponse(BaseModel):
    id: str
    reminder_time: datetime
    is_sent: bool
    notification_type: str
    created_at: Optional[datetime] = None
    todo_id: Optional[str] = None
    todo_title: Optional[str] = None
