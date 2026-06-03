import streamlit as st

from components.ui import metric_card, divider_label
from utils.api import get_notes, get_reminders, get_todos
from utils.auth import login_user, register_user
from utils.layout import load_styles, render_sidebar
from components.reminder_alerts import ensure_reminder_socket

st.set_page_config(
    page_title="VoiceNote AI",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_styles()
render_sidebar()

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "ws_started" not in st.session_state:
    st.session_state["ws_started"] = False

# ── Sign In / Sign Up ────────────────────────────────────────────────────────
if not st.session_state["authenticated"]:
    hero_col, form_col = st.columns([1.15, 1], gap="large")

    with hero_col:
        st.markdown(
            """
            <div class="auth-hero">
                <h1>🎙️ VoiceNote AI</h1>
                <p>
                    Capture thoughts by voice. The AI transcribes, classifies, and
                    files them as notes, todos, or reminders — automatically.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for label in ["Voice capture", "Smart todos", "Reminders", "Timeline", "Live alerts"]:
            st.markdown(f'<span class="feature-pill">{label}</span>', unsafe_allow_html=True)

        # Brief feature breakdown
        st.markdown(
            """
            <div style="margin-top:1.75rem;">
                <div style="display:flex;flex-direction:column;gap:0.65rem;">
                    <div style="display:flex;align-items:flex-start;gap:0.75rem;">
                        <span style="color:#4f8ef7;font-size:0.85rem;margin-top:0.05rem;">◆</span>
                        <div>
                            <span style="font-size:0.83rem;font-weight:600;color:#aab4c8;">Voice-first capture</span>
                            <p style="margin:0.15rem 0 0;font-size:0.77rem;color:#64748b;font-weight:300;">
                                Speak naturally — AI handles classification.
                            </p>
                        </div>
                    </div>
                    <div style="display:flex;align-items:flex-start;gap:0.75rem;">
                        <span style="color:#2dd4a0;font-size:0.85rem;margin-top:0.05rem;">◆</span>
                        <div>
                            <span style="font-size:0.83rem;font-weight:600;color:#aab4c8;">Live reminder alerts</span>
                            <p style="margin:0.15rem 0 0;font-size:0.77rem;color:#64748b;font-weight:300;">
                                In-app and desktop notifications via WebSocket.
                            </p>
                        </div>
                    </div>
                    <div style="display:flex;align-items:flex-start;gap:0.75rem;">
                        <span style="color:#f0b429;font-size:0.85rem;margin-top:0.05rem;">◆</span>
                        <div>
                            <span style="font-size:0.83rem;font-weight:600;color:#aab4c8;">Unified timeline</span>
                            <p style="margin:0.15rem 0 0;font-size:0.77rem;color:#64748b;font-weight:300;">
                                All items in one chronological view.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with form_col:
        tab_login, tab_signup = st.tabs(["Sign in", "Create account"])

        with tab_login:
            with st.form("login_form", clear_on_submit=False):
                email    = st.text_input("Email address", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                submitted = st.form_submit_button(
                    "Sign in", use_container_width=True, type="primary"
                )
            if submitted:
                success, msg = login_user(email, password)
                if success:
                    ensure_reminder_socket()
                    st.rerun()
                else:
                    st.error(f"Sign in failed: {msg}")

        with tab_signup:
            with st.form("signup_form"):
                reg_email    = st.text_input("Email address", key="reg_email", placeholder="you@example.com")
                reg_name     = st.text_input("Full name", placeholder="Jane Smith")
                reg_password = st.text_input("Password", type="password", key="reg_password", placeholder="••••••••")
                reg_submit   = st.form_submit_button("Create account", use_container_width=True)
            if reg_submit:
                success, msg = register_user(reg_email, reg_password, reg_name)
                if success:
                    st.success("Account created — sign in with your email.")
                else:
                    st.error(f"Registration failed: {msg}")


# ── Dashboard ────────────────────────────────────────────────────────────────
else:
    ensure_reminder_socket()
    notes     = get_notes()
    todos     = get_todos()
    reminders = get_reminders()
    pending   = sum(1 for t in todos if t.get("status") != "COMPLETED")

    st.markdown(
        """
        <div class="page-header">
            <div>
                <h1>Dashboard</h1>
                <p>Your workspace at a glance. Use Voice AI to add items hands-free.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Metric row
    m1, m2, m3, m4 = st.columns(4)
    with m1: metric_card("Notes",    len(notes),     "📝")
    with m2: metric_card("Open Todos", pending,       "✅")
    with m3: metric_card("Reminders", len(reminders), "⏰")
    with m4: metric_card("Voice AI",  "Ready",        "🎤")

    divider_label("Quick actions")

    a1, a2, a3, a4 = st.columns(4)
    with a1:
        st.markdown(
            '<div style="padding:0.85rem 1rem;background:rgba(255,255,255,0.03);'
            'border:1px solid rgba(255,255,255,0.07);border-radius:8px;margin-bottom:0.4rem;">'
            '<div style="font-size:1.25rem;margin-bottom:0.3rem;">🎤</div>'
            '<div style="font-size:0.82rem;font-weight:600;color:#aab4c8;margin-bottom:0.15rem;">Voice AI</div>'
            '<div style="font-size:0.75rem;color:#64748b;font-weight:300;">Speak to create any item.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.page_link("pages/5_Voice_AI.py", label="Open Voice AI", icon="🎤")
    with a2:
        st.markdown(
            '<div style="padding:0.85rem 1rem;background:rgba(255,255,255,0.03);'
            'border:1px solid rgba(255,255,255,0.07);border-radius:8px;margin-bottom:0.4rem;">'
            '<div style="font-size:1.25rem;margin-bottom:0.3rem;">📝</div>'
            '<div style="font-size:0.82rem;font-weight:600;color:#aab4c8;margin-bottom:0.15rem;">Notes</div>'
            '<div style="font-size:0.75rem;color:#64748b;font-weight:300;">Write or review saved notes.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.page_link("pages/1_Notes.py", label="Open Notes", icon="📝")
    with a3:
        st.markdown(
            '<div style="padding:0.85rem 1rem;background:rgba(255,255,255,0.03);'
            'border:1px solid rgba(255,255,255,0.07);border-radius:8px;margin-bottom:0.4rem;">'
            '<div style="font-size:1.25rem;margin-bottom:0.3rem;">✅</div>'
            '<div style="font-size:0.82rem;font-weight:600;color:#aab4c8;margin-bottom:0.15rem;">Todos</div>'
            '<div style="font-size:0.75rem;color:#64748b;font-weight:300;">Track tasks and mark done.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.page_link("pages/2_Todos.py", label="Open Todos", icon="✅")
    with a4:
        st.markdown(
            '<div style="padding:0.85rem 1rem;background:rgba(255,255,255,0.03);'
            'border:1px solid rgba(255,255,255,0.07);border-radius:8px;margin-bottom:0.4rem;">'
            '<div style="font-size:1.25rem;margin-bottom:0.3rem;">📅</div>'
            '<div style="font-size:0.82rem;font-weight:600;color:#aab4c8;margin-bottom:0.15rem;">Timeline</div>'
            '<div style="font-size:0.75rem;color:#64748b;font-weight:300;">Chronological overview.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.page_link("pages/4_Timeline.py", label="Open Timeline", icon="📅")

    # Recent activity
    recent = []
    for n in notes[:3]:
        n["_kind"] = "note"
        recent.append(n)
    for t in todos[:3]:
        t["_kind"] = "todo"
        recent.append(t)

    if recent:
        divider_label("Recent activity")
        for item in recent[:5]:
            if item["_kind"] == "note":
                preview = item.get("content", "")[:100]
                st.markdown(
                    f'<div style="display:flex;align-items:baseline;gap:0.6rem;'
                    f'padding:0.55rem 0;border-bottom:1px solid rgba(255,255,255,0.04);">'
                    f'<span style="font-size:0.68rem;font-weight:700;text-transform:uppercase;'
                    f'letter-spacing:0.08em;color:#4f8ef7;white-space:nowrap;">Note</span>'
                    f'<span style="font-size:0.85rem;color:#aab4c8;font-weight:300;">{preview}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div style="display:flex;align-items:baseline;gap:0.6rem;'
                    f'padding:0.55rem 0;border-bottom:1px solid rgba(255,255,255,0.04);">'
                    f'<span style="font-size:0.68rem;font-weight:700;text-transform:uppercase;'
                    f'letter-spacing:0.08em;color:#2dd4a0;white-space:nowrap;">Todo</span>'
                    f'<span style="font-size:0.85rem;color:#aab4c8;font-weight:300;">{item.get("title", "")}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
    else:
        st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)
        st.info("No activity yet — try Voice AI or add a note to get started.")