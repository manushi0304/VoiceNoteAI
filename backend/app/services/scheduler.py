import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.services.reminder_scheduler import ReminderSchedulerService


scheduler = AsyncIOScheduler()


def start_scheduler():
    scheduler.add_job(
        ReminderSchedulerService.process_due_reminders,
        "interval",
        seconds=30,
    )
    scheduler.start()
    print("⏰ Reminder scheduler started")
