from datetime import timedelta

import streamlit as st

from components.cards import reminder_card
from utils.api import create_reminder, delete_reminder, get_reminders
from utils.datetime_helpers import (
    combine_local,
    format_local_display,
    local_now,
    minutes_from_now,
    to_utc_iso,
    tomorrow_at,
)
from utils.layout import empty_state, load_styles, page_header, require_auth, render_sidebar

st.set_page_config(page_title="Reminders · VoiceNote AI", page_icon="⏰", layout="wide")
load_styles()
render_sidebar()
require_auth()

page_header(
    "Reminders",
    "All times in your local timezone. Alerts fire in-app and by email (~30 s check).",
    "⏰",
)

# ── Notification preference ──────────────────────────────────────────────────
NOTIFY_OPTIONS = {
    "In-app only":     "push",
    "Email only":      "email",
    "In-app + Email":  "both",
}

pref_col, _ = st.columns([2, 3])
with pref_col:
    notify_label = st.selectbox(
        "Notify via",
        options=list(NOTIFY_OPTIONS.keys()),
        index=2,
        help="Email requires SMTP settings in backend/.env — see README.",
    )
notify_type = NOTIFY_OPTIONS[notify_label]


def _schedule(iso_time: str, label: str) -> bool:
    ok, err = create_reminder(iso_time, notification_type=notify_type)
    if ok:
        st.success(f"Scheduled — {label}")
        st.rerun()
    st.error(err or "Could not schedule reminder.")
    return False


# ── Quick schedule ───────────────────────────────────────────────────────────
st.markdown(
    '<span style="font-size:0.7rem;font-weight:700;text-transform:uppercase;'
    'letter-spacing:0.1em;color:#3d4e68;display:block;margin-bottom:0.6rem;">Quick schedule</span>',
    unsafe_allow_html=True,
)

q1, q2, q3, q4 = st.columns(4)
if q1.button("In 5 min",       use_container_width=True): _schedule(minutes_from_now(5),  "5 minutes from now")
if q2.button("In 30 min",      use_container_width=True): _schedule(minutes_from_now(30), "30 minutes from now")
if q3.button("In 1 hour",      use_container_width=True): _schedule(minutes_from_now(60), "1 hour from now")
if q4.button("Tomorrow 9 AM",  use_container_width=True): _schedule(tomorrow_at(9, 0),    "tomorrow at 9:00 AM")

st.markdown('<div style="height:0.25rem;"></div>', unsafe_allow_html=True)

# ── Custom date/time ─────────────────────────────────────────────────────────
with st.form("new_reminder"):
    default_dt = local_now() + timedelta(hours=1)
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date", value=default_dt.date(), min_value=local_now().date())
    with col2:
        time = st.time_input("Time", value=default_dt.time())
    submitted = st.form_submit_button("Set reminder →", type="primary", use_container_width=True)

if submitted:
    reminder_local = combine_local(date, time)
    if reminder_local <= local_now() - timedelta(seconds=30):
        st.error("Pick a future date and time.")
    else:
        label = format_local_display(to_utc_iso(reminder_local))
        _schedule(to_utc_iso(reminder_local), label)

# ── List ─────────────────────────────────────────────────────────────────────
reminders = get_reminders()
upcoming  = [r for r in reminders if not r.get("is_sent")]
sent      = [r for r in reminders if r.get("is_sent")]

if not reminders:
    empty_state("⏰", "No reminders yet", "Schedule one above or ask Voice AI to remind you.")
else:
    if upcoming:
        st.markdown(
            '<span style="font-size:0.7rem;font-weight:700;text-transform:uppercase;'
            'letter-spacing:0.1em;color:#3d4e68;display:block;margin:1.25rem 0 0.75rem;">Upcoming</span>',
            unsafe_allow_html=True,
        )
        for reminder in upcoming:
            reminder_card(reminder, on_delete=delete_reminder)

    if sent:
        st.markdown(
            '<span style="font-size:0.7rem;font-weight:700;text-transform:uppercase;'
            'letter-spacing:0.1em;color:#3d4e68;display:block;margin:1.25rem 0 0.75rem;">Completed</span>',
            unsafe_allow_html=True,
        )
        for reminder in sent:
            reminder_card(reminder, on_delete=delete_reminder)