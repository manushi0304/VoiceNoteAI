# VoiceNote AI: REST API Documentation

This document outlines the API endpoints exposed by the VoiceNote AI backend. The API base URL is: `http://localhost:8000`.

---

## 🔐 Authentication Endpoints

All authenticated endpoints require a bearer JWT access token passed via the HTTP `Authorization: Bearer <TOKEN>` header.

### 1. Register User
- **Route**: `POST /auth/register`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword",
    "full_name": "John Doe"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "id": "1370544c-e906-487d-ac57-b9cab673563c",
    "email": "user@example.com"
  }
  ```

### 2. Login User (OAuth2)
- **Route**: `POST /auth/login`
- **Request Body (form-data)**:
  - `username`: Email string.
  - `password`: Password string.
- **Response (200 OK)**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1...",
    "token_type": "bearer"
  }
  ```

---

## 🎙️ Voice AI Endpoint

### 1. Upload Voice & Parse (Voice-first Capture)
- **Route**: `POST /voice-create/`
- **Headers**: `Authorization: Bearer <TOKEN>`
- **Request Body (multipart/form-data)**:
  - `file`: Audio file binary (e.g., `.wav`, `.mp3`).
- **Response (200 OK)**:
  ```json
  {
    "transcript": "buy milk tomorrow",
    "ml_prediction": "todo",
    "final_type": "todo",
    "confidence": 1.0,
    "created": true,
    "id": "7ac154ab-d926-4ee8-b892-a169b18362fa",
    "reminder_time": null,
    "language": "en"
  }
  ```

---

## 📝 Notes Endpoints

All routes require bearer JWT authentication.

- **`GET /notes`**: List all notes for the authenticated user.
- **`POST /notes`**: Create a manual note.
  - **Request Body**:
    ```json
    {
      "content": "Meeting notes regarding budget reviews.",
      "original_language": "en",
      "content_type": "note"
    }
    ```
- **`DELETE /notes/{note_id}`**: Delete notes by ID.

---

## ✅ Todos Endpoints

All routes require bearer JWT authentication.

- **`GET /todos/`**: List all tasks for the user.
- **`POST /todos/`**: Create a task.
  - **Request Body**:
    ```json
    {
      "title": "Buy groceries",
      "priority": "HIGH"
    }
    ```
- **`PATCH /todos/{todo_id}/toggle`**: Toggles a todo status between `PENDING` and `COMPLETED`.
- **`DELETE /todos/{todo_id}`**: Delete todo by ID.

---

## 📅 Reminders Endpoints

All routes require bearer JWT authentication.

- **`GET /reminders/`**: List scheduled reminders (sorted chronologically).
- **`POST /reminders/`**: Create a custom reminder alert.
  - **Request Body**:
    ```json
    {
      "reminder_time": "2026-06-02T18:30:00Z",
      "notification_type": "email"
    }
    ```
- **`DELETE /reminders/{reminder_id}`**: Delete reminder by ID.

---

## 🧠 NLP/ML Utility Endpoints

These endpoints are exposed for diagnostics, custom pipelines, and integrations.

### 1. Intent Classification
- **Route**: `POST /classify`
- **Request Body**:
  ```json
  {
    "text": "Buy groceries tomorrow at 8 AM"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "label": "todo",
    "confidence": 0.98
  }
  ```

### 2. Entity Extraction
- **Route**: `POST /extract-entities`
- **Request Body**:
  ```json
  {
    "text": "Call Sarah Smith regarding the contract next Monday"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "people": ["Sarah Smith"],
    "dates": ["next Monday"],
    "priority": "MEDIUM"
  }
  ```

### 3. Translate Text
- **Route**: `POST /translate`
- **Request Body**:
  ```json
  {
    "text": "Hello world",
    "source_language": "en",
    "target_language": "fr"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "translated_text": "Bonjour le monde"
  }
  ```

### 4. Parse Voice Command Intent
- **Route**: `POST /voice-command`
- **Request Body**:
  ```json
  {
    "text": "add groceries"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "intent": "create",
    "parameters": {
      "text": "add groceries"
    }
  }
  ```
