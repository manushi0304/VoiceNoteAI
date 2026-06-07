import pytest
import uuid
from datetime import datetime, timedelta, timezone
from httpx import AsyncClient

from app.core.database import AsyncSessionLocal
from app.schemas.auth import UserCreate
from app.services.auth_service import AuthService
from app.core.security import create_access_token

from app.services.note_service import NoteService
from app.schemas.note import NoteCreate

from app.services.todo_service import TodoService
from app.schemas.todo import TodoCreate

from app.services.reminder_service import ReminderService
from app.schemas.reminder import ReminderCreate


async def create_test_user():
    """Helper to register a unique user and return headers and user ID."""
    unique_email = f"crud_user_{uuid.uuid4().hex[:8]}@example.com"
    user_in = UserCreate(email=unique_email, password="password", full_name="CRUD User")
    
    async with AsyncSessionLocal() as db:
        user_res = await AuthService.register(db, user_in)
        user_id = user_res["id"]
        
    token = create_access_token(data={"sub": user_id})
    return {"Authorization": f"Bearer {token}"}, user_id


@pytest.mark.asyncio
async def test_notes_crud(client: AsyncClient):
    headers, user_id = await create_test_user()
    
    # 1. Service Create Note (isolated DB session)
    async with AsyncSessionLocal() as db:
        note_payload = NoteCreate(
            content="This is a test note content",
            original_language="en",
            content_type="note",
            classification_confidence=0.95
        )
        note = await NoteService.create(db, user_id, note_payload)
        note_id = note.id
        assert note.content == "This is a test note content"
    
    # 2. Service List Notes (isolated DB session)
    async with AsyncSessionLocal() as db:
        notes = await NoteService.list(db, user_id)
        assert len(notes) >= 1
        assert any(n.id == note_id for n in notes)
    
    # 3. Endpoint POST /notes (FastAPI client)
    api_payload = {
        "content": "API created note content",
        "original_language": "en",
        "content_type": "note",
        "classification_confidence": 0.85
    }
    response = await client.post("/notes", json=api_payload, headers=headers)
    assert response.status_code == 200
    created_note = response.json()
    assert created_note["content"] == "API created note content"
    
    # 4. Endpoint GET /notes (FastAPI client)
    response = await client.get("/notes", headers=headers)
    assert response.status_code == 200
    notes_list = response.json()
    assert len(notes_list) >= 2
    
    # 5. Endpoint DELETE /notes/{note_id} (FastAPI client)
    response = await client.delete(f"/notes/{created_note['id']}", headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_todos_crud(client: AsyncClient):
    headers, user_id = await create_test_user()
    
    # 1. Service Create Todo (isolated DB session)
    async with AsyncSessionLocal() as db:
        todo_payload = TodoCreate(
            title="Test Todo item",
            priority="HIGH"
        )
        todo = await TodoService.create(db, user_id, todo_payload)
        todo_id = todo.id
        assert todo.title == "Test Todo item"
        assert todo.priority.value == "HIGH"
    
    # 2. Service List Todos (isolated DB session)
    async with AsyncSessionLocal() as db:
        todos = await TodoService.list(db, user_id)
        assert len(todos) >= 1
        assert any(t["id"] == str(todo_id) for t in todos)
    
    # 3. Endpoint POST /todos/ (FastAPI client)
    api_payload = {
        "title": "API Todo item",
        "priority": "LOW"
    }
    response = await client.post("/todos/", json=api_payload, headers=headers)
    assert response.status_code == 200
    created_todo = response.json()
    assert created_todo["title"] == "API Todo item"
    
    # 4. Endpoint GET /todos/ (FastAPI client)
    response = await client.get("/todos/", headers=headers)
    assert response.status_code == 200
    todos_list = response.json()
    assert len(todos_list) >= 2
    
    # 5. Endpoint PATCH /todos/{todo_id}/toggle (FastAPI client)
    response = await client.patch(f"/todos/{created_todo['id']}/toggle", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "COMPLETED"
    
    # 5.5 Endpoint PATCH /todos/{todo_id}/priority (FastAPI client)
    response = await client.patch(f"/todos/{created_todo['id']}/priority", params={"priority": "HIGH"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["priority"] == "HIGH"
    
    # 6. Endpoint DELETE /todos/{todo_id} (FastAPI client)
    response = await client.delete(f"/todos/{created_todo['id']}", headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_reminders_crud(client: AsyncClient):
    headers, user_id = await create_test_user()
    
    # 1. Service Create Reminder with todo_title (isolated DB session)
    async with AsyncSessionLocal() as db:
        future_time = datetime.now(timezone.utc) + timedelta(hours=2)
        reminder_payload = ReminderCreate(
            reminder_time=future_time,
            notification_type="push",
            todo_title="Call Mom tomorrow"
        )
        reminder = await ReminderService.create(db, user_id, reminder_payload)
        reminder_id = reminder["id"]
        assert reminder["is_sent"] is False
        assert reminder["todo_title"] == "Call Mom tomorrow"
        assert reminder["todo_id"] is not None
    
    # 2. Service List Reminders (isolated DB session)
    async with AsyncSessionLocal() as db:
        reminders = await ReminderService.list(db, user_id)
        assert len(reminders) >= 1
        assert any(r["id"] == reminder_id for r in reminders)
        assert any(r["todo_title"] == "Call Mom tomorrow" for r in reminders)
    
    # 3. Endpoint POST /reminders/ with todo_title (FastAPI client)
    future_time_api = datetime.now(timezone.utc) + timedelta(days=1)
    api_payload = {
        "reminder_time": future_time_api.isoformat(),
        "notification_type": "push",
        "todo_title": "Finish presentation"
    }
    response = await client.post("/reminders/", json=api_payload, headers=headers)
    assert response.status_code == 200
    created_reminder = response.json()
    assert created_reminder["notification_type"] == "push"
    assert created_reminder["todo_title"] == "Finish presentation"
    assert created_reminder["todo_id"] is not None
    
    # 4. Endpoint GET /reminders/ (FastAPI client)
    response = await client.get("/reminders/", headers=headers)
    assert response.status_code == 200
    reminders_list = response.json()
    assert len(reminders_list) >= 2
    
    # 5. Endpoint DELETE /reminders/{reminder_id} (FastAPI client)
    response = await client.delete(f"/reminders/{created_reminder['id']}", headers=headers)
    assert response.status_code == 200
