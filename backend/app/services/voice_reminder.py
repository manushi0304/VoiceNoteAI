from datetime import datetime, timezone

import dateparser

from app.utils.datetime_utils import normalize_to_utc


def parse_reminder_time_from_text(text: str, entity_dates: list[str] | None = None) -> datetime | None:
    """
    Parse a future reminder time from natural language.
    Combines spaCy date/time entities first for maximum accuracy, then falls back to whole text.
    """
    settings = {
        "PREFER_DATES_FROM": "future",
        "RETURN_AS_TIMEZONE_AWARE": True,
        "RELATIVE_BASE": datetime.now(),
    }

    candidates: list[str] = []
    if entity_dates:
        # 1. Join all date/time entities together to form a clean combined phrase (e.g. "tomorrow 8am")
        combined = " ".join(entity_dates)
        if combined:
            candidates.append(combined)
        
        # 2. Add individual entities as fallback
        candidates.extend(entity_dates)
        
    # 3. Add the full utterance as final fallback
    candidates.append(text)

    for phrase in candidates:
        parsed = dateparser.parse(phrase, settings=settings)
        if parsed is None:
            continue
        utc = normalize_to_utc(parsed)
        if utc > datetime.now(timezone.utc):
            return utc

    return None

