import requests
import streamlit as st
import os

# Dynamic API selection: loads from environment variable (e.g., Streamlit Secrets) or falls back to localhost for local dev.
API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")


def auth_headers():
    token = st.session_state.get("token")

    if not token:
        return {}

    return {
        "Authorization": f"Bearer {token}"
    }


# ================= NOTES =================

def get_notes():
    r = requests.get(
        f"{API_BASE}/notes",
        headers=auth_headers()
    )

    if r.status_code == 200:
        return r.json()

    return []



def create_note(text: str):
    r = requests.post(
        f"{API_BASE}/notes",
        json={
            "content": text,
            "original_language": "en",
            "content_type": "note"
        },
        headers=auth_headers()
    )

    return r.status_code == 200



def delete_note(note_id: str):
    r = requests.delete(
        f"{API_BASE}/notes/{note_id}",
        headers=auth_headers()
    )

    return r.status_code == 200


# ================= TODOS =================

# ================= TODOS =================

def get_todos():

    r = requests.get(
        f"{API_BASE}/todos/",
        headers=auth_headers()
    )

    if r.status_code == 200:
        return r.json()

    return []


def create_todo(title: str, priority: str = "MEDIUM"):

    r = requests.post(
        f"{API_BASE}/todos/",
        json={
            "title": title,
            "priority": priority,
        },
        headers=auth_headers()
    )

    return r.status_code == 200


def delete_todo(todo_id: str):

    r = requests.delete(
        f"{API_BASE}/todos/{todo_id}",
        headers=auth_headers()
    )

    return r.status_code == 200


def toggle_todo(todo_id: str):

    r = requests.patch(
        f"{API_BASE}/todos/{todo_id}/toggle",
        headers=auth_headers()
    )

    return r.status_code == 200

# ================= REMINDERS =================

def get_reminders():
    r = requests.get(
        f"{API_BASE}/reminders/",
        headers=auth_headers()
    )

    if r.status_code == 200:
        return r.json()

    return []



def create_reminder(reminder_time: str, notification_type: str = "both", todo_title: str = None):
    payload = {
        "reminder_time": reminder_time,
        "notification_type": notification_type,
    }
    if todo_title:
        payload["todo_title"] = todo_title

    r = requests.post(
        f"{API_BASE}/reminders/",
        json=payload,
        headers=auth_headers(),
        timeout=15,
    )

    if r.status_code == 200:
        return True, None

    try:
        detail = r.json().get("detail", r.text)
        if isinstance(detail, list):
            detail = "; ".join(
                item.get("msg", str(item)) if isinstance(item, dict) else str(item)
                for item in detail
            )
    except Exception:
        detail = r.text
    return False, detail



def delete_reminder(reminder_id: str):
    r = requests.delete(
        f"{API_BASE}/reminders/{reminder_id}",
        headers=auth_headers()
    )

    return r.status_code == 200


# ================= TIMELINE =================

def get_timeline():
    notes = get_notes()
    todos = get_todos()
    reminders = get_reminders()

    timeline = []

    for n in notes:
        n["item_type"] = "note"
        timeline.append(n)

    for t in todos:
        t["item_type"] = "todo"
        timeline.append(t)

    for r in reminders:
        r["item_type"] = "reminder"
        timeline.append(r)

    def get_date(x):
        return x.get("created_at") or x.get("reminder_time") or ""

    timeline.sort(
        key=get_date,
        reverse=True
    )

    return timeline


def update_todo_priority(todo_id: str, priority: str):
    r = requests.patch(
        f"{API_BASE}/todos/{todo_id}/priority",
        params={"priority": priority},
        headers=auth_headers()
    )
    return r.status_code == 200