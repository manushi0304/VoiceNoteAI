from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    notes,
    todos,
    reminders,
    timeline,
    voice_create,
    ws,
    classify,
    extract,
    translate,
    voice_command
)

router = APIRouter()

router.include_router(auth.router, prefix="/auth")
router.include_router(notes.router, prefix="/notes")
router.include_router(todos.router, prefix="/todos")
router.include_router(reminders.router, prefix="/reminders")  # ✅ only here
router.include_router(voice_create.router, prefix="/voice-create")
router.include_router(timeline.router)
router.include_router(ws.router, prefix="/api/v1")

# Mount extra ML/NLP utility endpoints
router.include_router(classify.router)
router.include_router(extract.router)
router.include_router(translate.router)
router.include_router(voice_command.router)
