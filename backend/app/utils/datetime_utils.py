from datetime import datetime, timezone


def normalize_to_utc(dt: datetime) -> datetime:
    """Store all reminder times as timezone-aware UTC."""
    if dt.tzinfo is None:
        local_tz = datetime.now().astimezone().tzinfo
        dt = dt.replace(tzinfo=local_tz)
    return dt.astimezone(timezone.utc)
