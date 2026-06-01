from fastapi import APIRouter
from app.schemas.classification import ClassificationRequest, ClassificationResponse
from app.services.ai.classification import ClassificationService

router = APIRouter(prefix="/classify", tags=["Classification"])


@router.post("", response_model=ClassificationResponse)
async def classify_text(data: ClassificationRequest):
    return ClassificationService.classify(data.text)
