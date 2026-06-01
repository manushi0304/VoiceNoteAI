from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.models.note import Note
from fastapi import HTTPException

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.note import NoteCreate, NoteResponse
from app.services.note_service import NoteService
from app.models.user import User

router = APIRouter()


@router.post("", response_model=NoteResponse)
async def create_note(
    data: NoteCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await NoteService.create(db, user.id, data)


@router.get("", response_model=List[NoteResponse])
async def list_notes(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await NoteService.list(db, user.id)

@router.delete("/{note_id}")
async def delete_note(
    note_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):

    note = await db.get(Note, note_id)

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    await db.delete(note)
    await db.commit()

    return {"message": "Note deleted"}