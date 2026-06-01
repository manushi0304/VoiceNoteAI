from pydantic import BaseModel
from typing import Dict, Any


class VoiceCommandRequest(BaseModel):
    text: str


class VoiceCommandResponse(BaseModel):
    intent: str
    parameters: Dict[str, Any]
