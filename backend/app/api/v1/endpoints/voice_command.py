from fastapi import APIRouter
from app.schemas.voice_command import VoiceCommandRequest, VoiceCommandResponse
from app.services.ai.voice_parser import VoiceCommandService

router = APIRouter(prefix="/voice-command", tags=["Voice Commands"])


@router.post("", response_model=VoiceCommandResponse)
async def parse_voice_command(data: VoiceCommandRequest):
    parsed = VoiceCommandService.parse(data.text)
    return {
        "intent": parsed["intent"],
        "parameters": parsed.get("params", {})
    }
