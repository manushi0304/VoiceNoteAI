import streamlit as st

from utils.datetime_helpers import format_local_display


def _notify_label(nt: str) -> str:
    return {
        "push":      "In-app",
        "email":     "Email",
        "both":      "In-app + Email",
        "websocket": "In-app",
    }.get(nt or "", nt or "—")


def reminder_card(reminder, on_delete=None):
    when = format_local_display(reminder.get("reminder_time", ""))
    is_sent = reminder.get("is_sent", False)
    status_html = (
        '<span class="status-badge sent">Sent</span>'
        if is_sent else
        '<span class="status-badge success">Scheduled</span>'
    )
    via = _notify_label(reminder.get("notification_type", ""))
    created = format_local_display(reminder.get("created_at", ""))
    todo_title = reminder.get("todo_title")
    title_html = (
        f'<h4 style="margin: 0 0 0.4rem 0; font-size: 1.05rem; font-weight: 600; color: #e8edf5;">{todo_title}</h4>'
        if todo_title else
        '<h4 style="margin: 0 0 0.4rem 0; font-size: 1.05rem; font-weight: 600; color: #a3b3c9; font-style: italic;">Quick Reminder</h4>'
    )

    with st.container():
        st.markdown(
            f"""
            <div class="item-card">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.5rem;">
                    <span class="card-type">⏰ &nbsp;Reminder</span>
                    {status_html}
                </div>
                {title_html}
                <p class="card-body" style="font-size:0.9rem; color:#a3b3c9; margin: 0 0 0.5rem 0;">⏰ {when}</p>
                <div class="card-meta">via {via} &nbsp;·&nbsp; created {created}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if on_delete:
            cols = st.columns([6, 1])
            with cols[1]:
                if st.button("✕", key=f"reminder_{reminder['id']}", help="Delete reminder"):
                    on_delete(reminder["id"])
                    st.rerun()


def note_card(note, on_delete=None):
    content = note.get("content", "")
    created = format_local_display(note.get("created_at", ""))
    preview = content if len(content) <= 300 else content[:297] + "…"

    with st.container():
        st.markdown(
            f"""
            <div class="item-card">
                <div class="card-type">📝 &nbsp;Note</div>
                <p class="card-body">{preview}</p>
                <div class="card-meta">{created}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if on_delete:
            cols = st.columns([6, 1])
            with cols[1]:
                if st.button("✕", key=f"note_{note['id']}", help="Delete note"):
                    on_delete(note["id"])
                    st.rerun()


def todo_card(todo, on_delete=None, on_toggle=None, on_priority_change=None):
    is_completed = todo.get("status") == "COMPLETED"
    priority = (todo.get("priority") or "normal").lower()
    created = format_local_display(todo.get("created_at", ""))

    priority_colors = {
        "high":   ("#f56565", "rgba(245,101,101,0.12)"),
        "normal": ("#4f8ef7", "rgba(79,142,247,0.08)"),
        "low":    ("#64748b", "rgba(100,116,139,0.08)"),
    }
    p_color, p_bg = priority_colors.get(priority, priority_colors["normal"])

    with st.container():
        col_check, col_del = st.columns([11, 1])

        with col_check:
            checked = st.checkbox(
                todo.get("title", "Untitled"),
                value=is_completed,
                key=f"todo_{todo['id']}",
            )
            if checked != is_completed and on_toggle:
                on_toggle(todo["id"])
                st.rerun()

            badge_html = (
                '<span class="status-badge success">Done</span>'
                if is_completed else
                f'<span style="display:inline-flex;align-items:center;'
                f'background:{p_bg};color:{p_color};'
                f'border:1px solid {p_color}44;'
                f'padding:0.15rem 0.45rem;border-radius:4px;'
                f'font-size:0.68rem;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;">'
                f'{priority} priority</span>'
            )
            st.markdown(
                f'{badge_html} &nbsp;<span style="font-size:0.7rem;color:#3d4e68;'
                f'font-family:var(--font-mono,monospace);">{created}</span>',
                unsafe_allow_html=True,
            )

            # Option to change priority if not completed
            if not is_completed and on_priority_change:
                cols_p = st.columns([3, 5])
                with cols_p[0]:
                    current_p = todo.get("priority", "MEDIUM").upper()
                    if current_p not in ["HIGH", "MEDIUM", "LOW"]:
                        current_p = "MEDIUM"
                    current_p_index = ["HIGH", "MEDIUM", "LOW"].index(current_p)
                    
                    new_priority = st.selectbox(
                        "Change priority",
                        options=["HIGH", "MEDIUM", "LOW"],
                        index=current_p_index,
                        key=f"priority_change_select_{todo['id']}",
                        label_visibility="collapsed"
                    )
                    if new_priority.upper() != current_p:
                        on_priority_change(todo["id"], new_priority)
                        st.rerun()

        with col_del:
            if on_delete:
                if st.button("✕", key=f"delete_{todo['id']}", help="Delete todo"):
                    on_delete(todo["id"])
                    st.rerun()