from pydantic import BaseModel
from typing import List


class ExtractionRequest(BaseModel):
    text: str


class ExtractionResponse(BaseModel):
    people: List[str]
    dates: List[str]
    priority: str
