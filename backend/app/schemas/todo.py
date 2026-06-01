from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class TodoStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    priority: Priority = Priority.MEDIUM
    due_date: datetime | None = None
    note_id: UUID | None = None


class TodoResponse(TodoCreate):
    id: UUID
    user_id: UUID
    status: TodoStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
