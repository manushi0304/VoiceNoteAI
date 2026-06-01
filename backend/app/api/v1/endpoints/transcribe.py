from fastapi import APIRouter, UploadFile, File
from app.services.ai.transcription import TranscriptionService

router = APIRouter(prefix="/transcribe", tags=["Speech-to-Text"])


@router.post("")
async def transcribe_audio(file: UploadFile = File(...)):
    path = f"/tmp/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    return TranscriptionService.transcribe(path)
