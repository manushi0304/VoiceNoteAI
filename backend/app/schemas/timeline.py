from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID


class TimelineItem(BaseModel):
    id: UUID
    type: str
    text: str
    extra: Optional[Dict[str, Any]] = {}
    created_at: datetime
