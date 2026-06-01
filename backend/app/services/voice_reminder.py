from datetime import datetime, timezone

import dateparser

from app.utils.datetime_utils import normalize_to_utc


def parse_reminder_time_from_text(text: str, entity_dates: list[str] | None = None) -> datetime | None:
    """
    Parse a future reminder time from natural language.
    Tries the full utterance first, then spaCy date entities.
    """
    settings = {
        "PREFER_DATES_FROM": "future",
        "RETURN_AS_TIMEZONE_AWARE": True,
        "RELATIVE_BASE": datetime.now(),
    }

    candidates: list[str] = [text]
    if entity_dates:
        candidates.extend(entity_dates)

    for phrase in candidates:
        parsed = dateparser.parse(phrase, settings=settings)
        if parsed is None:
            continue
        utc = normalize_to_utc(parsed)
        if utc > datetime.now(timezone.utc):
            return utc

    return None
