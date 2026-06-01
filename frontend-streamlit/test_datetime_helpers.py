import pytest
from datetime import datetime, date, time, timedelta, timezone
from utils.datetime_helpers import (
    combine_local,
    to_utc_iso,
    format_local_display,
    minutes_from_now,
    tomorrow_at,
    local_now
)


def test_local_now():
    now = local_now()
    assert isinstance(now, datetime)
    assert now.tzinfo is not None


def test_combine_local():
    d = date(2026, 6, 1)
    t = time(12, 30)
    dt = combine_local(d, t)
    assert dt.date() == d
    assert dt.time() == t
    assert dt.tzinfo == local_now().tzinfo


def test_to_utc_iso():
    dt = datetime(2026, 6, 1, 12, 30, tzinfo=timezone.utc)
    iso = to_utc_iso(dt)
    assert "2026-06-01T12:30:00+00:00" in iso or "2026-06-01T12:30:00Z" in iso


def test_format_local_display():
    iso_utc = "2026-06-01T12:30:00+00:00"
    display = format_local_display(iso_utc)
    assert display != ""
    assert isinstance(display, str)

    # Test empty or invalid values safety
    assert format_local_display("") == ""
    assert format_local_display("invalid-date-string") == "invalid-date-string"


def test_minutes_from_now():
    iso = minutes_from_now(10)
    assert isinstance(iso, str)
    # Verify that it parses back to a UTC datetime
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    assert dt.tzinfo == timezone.utc


def test_tomorrow_at():
    iso = tomorrow_at(15, 45)
    assert isinstance(iso, str)
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    assert dt.tzinfo == timezone.utc
