"""Live reminder pop-ups: in-app toasts + optional browser notifications."""

import json
from datetime import timedelta

import streamlit as st
import streamlit.components.v1 as components

from utils.datetime_helpers import format_local_display
from utils.notifications import drain_reminders
from utils.websocket import ReminderSocket


def ensure_reminder_socket():
    if st.session_state.get("authenticated") and not st.session_state.get("ws_started"):
        ReminderSocket(st.session_state["token"]).start()
        st.session_state["ws_started"] = True


def _browser_notify(title: str, body: str):
    components.html(
        f"""
        <script>
        (function() {{
            const title = {json.dumps(title)};
            const body = {json.dumps(body)};
            if (!("Notification" in window)) return;
            const fire = () => new Notification(title, {{
                body: body,
                tag: "voicenote-reminder",
            }});
            if (Notification.permission === "granted") {{
                fire();
            }} else if (Notification.permission !== "denied") {{
                Notification.requestPermission().then((p) => {{
                    if (p === "granted") fire();
                }});
            }}
        }})();
        </script>
        """,
        height=0,
    )


def _request_notification_permission():
    components.html(
        """
        <script>
        if ("Notification" in window && Notification.permission === "default") {
            Notification.requestPermission();
        }
        </script>
        """,
        height=0,
    )


def _process_reminder(payload: dict):
    message = payload.get("message", "Your scheduled reminder is due.")
    when = payload.get("time", "")
    when_local = format_local_display(when) if when else "now"
    title = "VoiceNote AI — Reminder"
    body = f"{message} · {when_local}" if when_local else message

    st.toast(body, icon="⏰")

    if st.session_state.get("browser_notifications", True):
        _browser_notify(title, body)

    alerts = st.session_state.setdefault("recent_reminder_alerts", [])
    alerts.insert(0, {"title": title, "body": body, "when": when_local})
    st.session_state["recent_reminder_alerts"] = alerts[:5]


def _poll_reminder_queue():
    for payload in drain_reminders():
        _process_reminder(payload)


if hasattr(st, "fragment"):

    @st.fragment(run_every=timedelta(seconds=3))
    def reminder_ws_listener():
        if st.session_state.get("authenticated"):
            _poll_reminder_queue()

else:

    def reminder_ws_listener():
        pass


def render_reminder_listener():
    ensure_reminder_socket()
    if not st.session_state.get("authenticated"):
        return
    _poll_reminder_queue()
    reminder_ws_listener()


def render_reminder_sidebar_controls():
    if not st.session_state.get("authenticated"):
        return

    st.caption("Reminder alerts")
    enabled = st.toggle(
        "Desktop pop-ups",
        value=st.session_state.get("browser_notifications", True),
        help="System notifications when a reminder is due.",
    )
    st.session_state["browser_notifications"] = enabled

    if st.button("Allow notifications", use_container_width=True, type="secondary"):
        _request_notification_permission()
        st.toast("Check your browser for the permission prompt.", icon="🔔")


def render_recent_alert_banner():
    alerts = st.session_state.get("recent_reminder_alerts") or []
    if not alerts:
        return

    latest = alerts[0]
    st.markdown(
        f"""
        <div class="reminder-alert-banner">
            <strong>⏰ {latest["title"]}</strong><br/>
            <span>{latest["body"]}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )