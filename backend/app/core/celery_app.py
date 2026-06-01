from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "voicenote_ai",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.task_track_started = True
celery_app.conf.result_extended = True
