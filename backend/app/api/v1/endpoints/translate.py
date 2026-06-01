from fastapi import APIRouter
from app.schemas.translation import TranslationRequest, TranslationResponse
from app.services.ai.translation import TranslationService

router = APIRouter(prefix="/translate", tags=["Translation"])


@router.post("", response_model=TranslationResponse)
async def translate_text(data: TranslationRequest):
    text = TranslationService.translate(
        data.text, data.source_language, data.target_language
    )
    return {"translated_text": text}
