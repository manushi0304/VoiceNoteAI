from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.timeline_service import TimelineService

router = APIRouter(
    prefix="/timeline",
    tags=["Timeline"],
)


@router.get("/")
async def get_timeline(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await TimelineService.get_timeline(db, user.id)
