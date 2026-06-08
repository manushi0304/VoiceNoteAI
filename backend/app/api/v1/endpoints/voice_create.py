from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
)

from sqlalchemy.ext.asyncio import AsyncSession

import tempfile
import os

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.services.ai.transcription import (
    TranscriptionService
)
from app.utils.text_cleaning import clean_voice_text

from app.services.ai.extraction import (
    ExtractionService
)

from app.services.note_service import (
    NoteService
)

from app.services.todo_service import (
    TodoService
)

from app.services.reminder_service import (
    ReminderService
)

from app.services.classifier_service import (
    TextClassifierService
)

from app.services.voice_reminder import (
    parse_reminder_time_from_text
)

from app.schemas.note import NoteCreate
from app.schemas.todo import TodoCreate
from app.schemas.reminder import ReminderCreate

from app.models.user import User

router = APIRouter(tags=["Voice AI"])

# =====================================================
# LOAD CLASSIFIER ONCE
# =====================================================
classifier = TextClassifierService()


@router.post("/")
async def voice_create(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    audio_path = None

    try:

        # =====================================================
        # SAVE AUDIO
        # =====================================================
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as tmp:

            tmp.write(await file.read())
            audio_path = tmp.name

        # =====================================================
        # TRANSCRIBE AUDIO
        # =====================================================
        transcript = TranscriptionService.transcribe(
            audio_path
        )

        text = transcript.get(
            "text",
            ""
        ).strip()

        if not text:

            raise HTTPException(
                status_code=400,
                detail="Empty transcription"
            )

        # =====================================================
        # ALWAYS RUN ML MODEL
        # =====================================================
        ml_label, ml_confidence = (
            classifier.predict(text)
        )

        print("\n========== ML DEBUG ==========")
        print("INPUT:", text)
        print("ML LABEL:", ml_label)
        print("ML CONFIDENCE:", ml_confidence)

        # =====================================================
        # RULE-BASED OVERRIDE
        # =====================================================
        lower_text = text.lower()

        if (
            "remind" in lower_text
            or "mind me" in lower_text
            or "reminder" in lower_text
        ):

            label = "reminder"
            confidence = 1.0

            print(
                "FINAL LABEL: reminder (RULE)"
            )

        elif (
            "note" in lower_text
            or "notes" in lower_text
            or "write down" in lower_text
            or "journal" in lower_text
        ):

            label = "note"
            confidence = 1.0

            print(
                "FINAL LABEL: note (RULE)"
            )

        elif (
            "buy" in lower_text
            or "todo" in lower_text
            or "to do" in lower_text
            or "to-do" in lower_text
            or "complete" in lower_text
            or "finish" in lower_text
            or "task" in lower_text
        ):

            label = "todo"
            confidence = 1.0

            print(
                "FINAL LABEL: todo (RULE)"
            )

        else:

            label = ml_label
            confidence = ml_confidence

            print(
                f"FINAL LABEL: {label} (ML)"
            )

        # =====================================================
        # CONFIDENCE CHECK
        # =====================================================
        if confidence < 0.60:

            raise HTTPException(
                status_code=400,
                detail=(
                    f"Low classification "
                    f"confidence ({confidence:.2f})"
                ),
            )

        # =====================================================
        # ENTITY EXTRACTION
        # =====================================================
        entities = (
            ExtractionService.extract(text)
        )

        result = None

        # =====================================================
        # CREATE NOTE
        # =====================================================
        if label == "note":

            cleaned_text = clean_voice_text(text, label)
            payload = NoteCreate(
                content=cleaned_text,
                original_language=transcript.get(
                    "language",
                    "en"
                ),
                content_type="note",
                classification_confidence=float(
                    confidence
                ),
            )

            result = await NoteService.create(
                db,
                user.id,
                payload,
            )

        # =====================================================
        # CREATE TODO
        # =====================================================
        elif label == "todo":

            cleaned_text = clean_voice_text(text, label)
            payload = TodoCreate(
                title=cleaned_text,
                priority=entities.get(
                    "priority",
                    "MEDIUM"
                ),
            )

            result = await TodoService.create(
                db,
                user.id,
                payload,
            )

        # =====================================================
        # CREATE REMINDER
        # =====================================================
        elif label == "reminder":

            reminder_time = (
                parse_reminder_time_from_text(
                    text,
                    entities.get("dates"),
                )
            )

            if not reminder_time:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Could not extract "
                        "a future reminder time. "
                        "Try: 'Remind me tomorrow "
                        "at 8pm'"
                    ),
                )

            cleaned_text = clean_voice_text(text, label)
            payload = ReminderCreate(
                reminder_time=reminder_time,
                notification_type="both",
                todo_title=cleaned_text,
            )

            result = await ReminderService.create(
                db,
                user.id,
                payload,
            )

        else:

            raise HTTPException(
                status_code=400,
                detail="Unsupported content type",
            )

        # =====================================================
        # RESPONSE
        # =====================================================
        if isinstance(result, dict):

            created_id = result.get("id")

            reminder_value = result.get(
                "reminder_time"
            )

        else:

            created_id = str(result.id)

            reminder_value = None

        return {

            "transcript": text,

            "ml_prediction": ml_label,

            "final_type": label,

            "confidence": float(confidence),

            "created": True,

            "id": created_id,

            "reminder_time": reminder_value,

            "language": transcript.get(
                "language",
                "unknown"
            ),
        }

    except HTTPException:
        raise

    except Exception as e:

        print(
            "\nVOICE CREATE ERROR:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    finally:

        # =====================================================
        # CLEANUP
        # =====================================================
        if (
            audio_path
            and os.path.exists(audio_path)
        ):
            os.unlink(audio_path)