from pathlib import Path

import streamlit as st

from components.reminder_alerts import (
    render_recent_alert_banner,
    render_reminder_listener,
    render_reminder_sidebar_controls,
)
from utils.api import get_notes, get_reminders, get_todos

CSS_PATH = Path(__file__).resolve().parent.parent / "styles.css"


def load_styles():
    css = CSS_PATH.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    render_reminder_listener()
    if st.session_state.get("authenticated"):
        render_recent_alert_banner()


def require_auth():
    if not st.session_state.get("authenticated"):
        st.markdown(
            """
            <div style="text-align:center;padding:3rem 1rem;">
                <div style="font-size:2rem;margin-bottom:0.75rem;opacity:0.4;">🔐</div>
                <p style="color:var(--text-muted,#64748b);font-size:0.88rem;margin:0 0 1rem;">
                    Sign in to access your workspace.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link("app.py", label="Go to sign in", icon="🔐")
        st.stop()


def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <span class="brand-icon">🎙️</span>
                <div>
                    <div class="brand-title">VoiceNote AI</div>
                    <div class="brand-sub">Productivity workspace</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.get("authenticated"):
            notes     = get_notes()
            todos     = get_todos()
            reminders = get_reminders()
            pending   = sum(1 for t in todos if t.get("status") != "COMPLETED")

            # Compact stats row
            st.markdown(
                f"""
                <div style="
                    display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.4rem;
                    margin:0.75rem 0 1rem;
                ">
                    <div style="
                        background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
                        border-radius:6px;padding:0.55rem 0.5rem;text-align:center;
                    ">
                        <div style="font-size:1.1rem;font-weight:700;color:#e8edf5;
                                    font-family:'Cormorant Garamond',serif;">{len(notes)}</div>
                        <div style="font-size:0.6rem;font-weight:600;text-transform:uppercase;
                                    letter-spacing:0.08em;color:#64748b;margin-top:0.15rem;">Notes</div>
                    </div>
                    <div style="
                        background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
                        border-radius:6px;padding:0.55rem 0.5rem;text-align:center;
                    ">
                        <div style="font-size:1.1rem;font-weight:700;color:#e8edf5;
                                    font-family:'Cormorant Garamond',serif;">{pending}</div>
                        <div style="font-size:0.6rem;font-weight:600;text-transform:uppercase;
                                    letter-spacing:0.08em;color:#64748b;margin-top:0.15rem;">Open</div>
                    </div>
                    <div style="
                        background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
                        border-radius:6px;padding:0.55rem 0.5rem;text-align:center;
                    ">
                        <div style="font-size:1.1rem;font-weight:700;color:#e8edf5;
                                    font-family:'Cormorant Garamond',serif;">{len(reminders)}</div>
                        <div style="font-size:0.6rem;font-weight:600;text-transform:uppercase;
                                    letter-spacing:0.08em;color:#64748b;margin-top:0.15rem;">Alerts</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
            render_reminder_sidebar_controls()

            st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)

            if st.button("Sign out", use_container_width=True, type="secondary"):
                st.session_state.clear()
                st.rerun()
        else:
            st.markdown(
                '<p style="font-size:0.78rem;color:#3d4e68;line-height:1.6;margin:0.75rem 0 0;">'
                'Sign in to unlock Notes, Todos, Reminders, and Voice AI.'
                '</p>',
                unsafe_allow_html=True,
            )


def page_header(title: str, subtitle: str, icon: str = ""):
    label = f"{icon}&nbsp;{title}".strip() if icon else title
    st.markdown(
        f"""
        <div class="page-header">
            <div>
                <h1>{label}</h1>
                <p>{subtitle}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state(icon: str, title: str, hint: str):
    st.markdown(
        f"""
        <div class="empty-state">
            <span class="empty-icon">{icon}</span>
            <h3>{title}</h3>
            <p>{hint}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )