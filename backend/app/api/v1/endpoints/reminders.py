from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.reminder import Reminder
from app.models.user import User
from app.schemas.reminder import ReminderCreate
from app.services.reminder_service import ReminderService

router = APIRouter(tags=["Reminders"])


@router.get("/")
async def list_reminders(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await ReminderService.list(db, user.id)


@router.post("/")
async def create_reminder(
    payload: ReminderCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await ReminderService.create(db, user.id, payload)

@router.delete("/{reminder_id}")
async def delete_reminder(
    reminder_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):

    reminder = await db.get(
        Reminder,
        reminder_id
    )

    if not reminder:
        raise HTTPException(
            status_code=404,
            detail="Reminder not found"
        )

    await db.delete(reminder)
    await db.commit()

    return {"message": "Reminder deleted"}