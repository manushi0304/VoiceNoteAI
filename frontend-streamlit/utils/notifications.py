import queue

reminder_queue: queue.Queue = queue.Queue()


def push_reminder(payload: dict):
    reminder_queue.put(payload)


def drain_reminders() -> list[dict]:
    items = []
    while not reminder_queue.empty():
        try:
            items.append(reminder_queue.get_nowait())
        except queue.Empty:
            break
    return items