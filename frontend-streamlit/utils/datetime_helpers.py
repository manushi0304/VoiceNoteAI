from datetime import datetime, timedelta, timezone


def local_now() -> datetime:
    return datetime.now().astimezone()


def combine_local(date, time) -> datetime:
    """Combine date + time as local timezone-aware datetime."""
    naive = datetime.combine(date, time)
    return naive.replace(tzinfo=local_now().tzinfo)


def to_utc_iso(dt: datetime) -> str:
    """API payload: always UTC with offset."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=local_now().tzinfo)
    return dt.astimezone(timezone.utc).isoformat()


def format_local_display(iso_value: str) -> str:
    if not iso_value:
        return ""
    try:
        dt = datetime.fromisoformat(iso_value.replace("Z", "+00:00"))
        return dt.astimezone().strftime("%a, %b %d · %I:%M %p")
    except (ValueError, TypeError):
        return str(iso_value)


def minutes_from_now(minutes: int) -> str:
    return to_utc_iso(local_now() + timedelta(minutes=minutes))


def tomorrow_at(hour: int, minute: int = 0) -> str:
    tomorrow = local_now().date() + timedelta(days=1)
    t = datetime.strptime(f"{hour:02d}:{minute:02d}", "%H:%M").time()
    return to_utc_iso(combine_local(tomorrow, t))