from fastapi import APIRouter
from app.schemas.extraction import ExtractionRequest, ExtractionResponse
from app.services.ai.extraction import ExtractionService

router = APIRouter(prefix="/extract-entities", tags=["Entity Extraction"])


@router.post("", response_model=ExtractionResponse)
async def extract_entities(data: ExtractionRequest):
    return ExtractionService.extract(data.text)
