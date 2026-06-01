# VoiceNote AI: Deployment & Operations Guide

This document outlines deployment configurations, background task runners, queues, and containerization instructions for VoiceNote AI.

---

## 📦 Containerized Orchestration (Docker)

The project supports orchestrating both cache stores, email brokers, and relational engines using lightweight Docker container configurations.

### Database Engine (PostgreSQL + pgvector)
A customized PostgreSQL database running `pgvector` provides core relational operations and vector embedding indexing:
- **Port**: `5433`
- **Dialect**: `postgresql+asyncpg`
- **Volume Mapping**: Relational tables and indices are mapped locally to keep data persistent across container reboots.

### Message Broker (Redis)
Redis serves as the caching broker for distributing async alerts:
- **Port**: `6379`
- **Volume Mapping**: Keeps queue states persistent.

---

## ⏰ Background Scheduling & Workers

VoiceNote AI processes reminder alerts asynchronously using `Celery` task runners and the `APScheduler` background service:

### 1. Scheduler Daemon
- **Script**: `backend/app/services/scheduler.py`
- **Purpose**: A lightweight background daemon launched on FastAPI startup. It runs active cron polling tasks every **60 seconds** to scan the PostgreSQL database for reminders that are due.
- **Workflow**:
  1. Scheduler queries for un-sent reminders where `reminder_time <= NOW()`.
  2. If found, a background Celery task is dispatched to the Redis broker, and the database reminder state is flagged as sent (`is_sent = True`).

### 2. Celery Worker Tasks
- **Worker Run Command**:
  ```bash
  cd backend
  .\venv\Scripts\celery.exe -A app.core.celery_app worker --loglevel=info
  ```
- **Task Handlers**:
  - **Email Alerts**: Formats and dispatches Gmail HTML alerts to target users using secure SMTP transport.
  - **WebSocket Alerts**: Dispatches real-time in-app dashboard alert notifications to active Streamlit connection states.

---

## 🚀 Standard Production Deployment Steps

1. **Clone & Set Up Environment**:
   Clone the repository and copy the environment parameters into `backend/.env`. Exclude this file from public git commits.
2. **Apply Migrations**:
   Run database schema creation:
   ```bash
   cd backend
   .\venv\Scripts\alembic.exe upgrade head
   ```
3. **Launch Workers**:
   Start Redis, database containers, and Celery background workers.
4. **Deploy Application**:
   Expose the backend port `8000` behind a reverse proxy (e.g. Nginx with secure SSL certificates) and run the Streamlit dashboard on port `8501`.
