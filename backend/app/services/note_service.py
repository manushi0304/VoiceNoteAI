from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models.note import Note
from app.schemas.note import NoteCreate


class NoteService:
    @staticmethod
    async def create(db: AsyncSession, user_id: UUID, data: NoteCreate) -> Note:
        note = Note(user_id=user_id, **data.dict())
        db.add(note)
        await db.commit()
        await db.refresh(note)
        return note

    @staticmethod
    async def list(db: AsyncSession, user_id: UUID) -> list[Note]:
        result = await db.execute(select(Note).where(Note.user_id == user_id))
        return result.scalars().all()
