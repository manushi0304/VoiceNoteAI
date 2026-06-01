from pydantic import BaseModel
from typing import List


class TranscriptionSegment(BaseModel):
    text: str
    start: float
    end: float


class TranscriptionResponse(BaseModel):
    text: str
    language: str
    segments: List[TranscriptionSegment]
