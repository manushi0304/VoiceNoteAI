from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.todo import Todo, TodoStatus

from app.schemas.todo import TodoCreate

from app.services.todo_service import TodoService

router = APIRouter(tags=["Todos"])


# =====================================================
# GET TODOS
# =====================================================
@router.get("/")
async def list_todos(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await TodoService.list(
        db,
        user.id
    )


# =====================================================
# CREATE TODO
# =====================================================
@router.post("/")
async def create_todo(
    payload: TodoCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await TodoService.create(
        db,
        user.id,
        payload
    )


# =====================================================
# DELETE TODO
# =====================================================
@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):

    todo = await db.get(Todo, todo_id)

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    await db.delete(todo)
    await db.commit()

    return {
        "message": "Todo deleted"
    }


# =====================================================
# TOGGLE COMPLETE
# =====================================================
@router.patch("/{todo_id}/toggle")
async def toggle_todo(
    todo_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):

    todo = await db.get(Todo, todo_id)

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    # ---------------- TOGGLE ----------------
    if todo.status == TodoStatus.COMPLETED:

        todo.status = TodoStatus.PENDING
        todo.completed_at = None

    else:

        todo.status = TodoStatus.COMPLETED
        todo.completed_at = datetime.utcnow()

    await db.commit()
    await db.refresh(todo)

    return {
        "id": str(todo.id),
        "status": todo.status.value
    }


# =====================================================
# UPDATE PRIORITY
# =====================================================
@router.patch("/{todo_id}/priority")
async def update_priority(
    todo_id: str,
    priority: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    from app.models.todo import Priority

    todo = await db.get(Todo, todo_id)

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    try:
        todo.priority = Priority(priority.upper())
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid priority '{priority}'. Must be one of HIGH, MEDIUM, LOW."
        )

    await db.commit()
    await db.refresh(todo)

    return {
        "id": str(todo.id),
        "priority": todo.priority.value
    }