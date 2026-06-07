from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_v1_router
from app.services.scheduler import start_scheduler
from app.middleware.logging import LoggingMiddleware
from app.middleware.auth_middleware import AuthMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)

@app.on_event("startup")
async def startup():
    print("🚀 VoiceNote AI backend starting up...")
    start_scheduler()
    import os
    if os.getenv("RENDER") != "true":
        try:
            from app.services.ai.transcription import get_model
            # Pre-load Whisper model to avoid 30s request timeouts in local dev
            get_model()
        except Exception as e:
            print(f"⚠️ Failed to preload Whisper model on startup: {e}")


# Middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8501",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(api_v1_router)


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
