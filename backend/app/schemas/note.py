from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Dict,Optional
from enum import Enum


class ContentType(str, Enum):
    note = "note"
    todo = "todo"
    reminder = "reminder"


class NoteCreate(BaseModel):
    title: str | None = None
    content: str
    original_language: str
    translated_content: Dict[str, str] | None = None
    content_type: ContentType
    classification_confidence: Optional[float] = None
    audio_url: str | None = None


class NoteResponse(NoteCreate):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
