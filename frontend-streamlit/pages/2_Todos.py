import streamlit as st

from components.cards import todo_card
from utils.api import create_todo, delete_todo, get_todos, toggle_todo, update_todo_priority
from utils.layout import empty_state, load_styles, page_header, require_auth, render_sidebar

st.set_page_config(page_title="Todos · VoiceNote AI", page_icon="✅", layout="wide")
load_styles()
render_sidebar()
require_auth()

page_header("Todos", "Track tasks and mark them done when finished.", "✅")

with st.form("new_todo", clear_on_submit=True):
    col_t, col_p = st.columns([3, 1])
    with col_t:
        title = st.text_input("New task", placeholder="What needs to get done?")
    with col_p:
        priority = st.selectbox("Priority", ["HIGH", "MEDIUM", "LOW"], index=1)
    submitted = st.form_submit_button("Add todo →", type="primary", use_container_width=True)

if submitted:
    if title.strip():
        if create_todo(title, priority):
            st.rerun()
        else:
            st.error("Could not add todo. Check the API.")
    else:
        st.warning("Enter a title first.")

st.markdown('<div style="height:0.25rem;"></div>', unsafe_allow_html=True)

todos = get_todos()
total     = len(todos)
pending   = sum(1 for t in todos if t.get("status") != "COMPLETED")
completed = total - pending

# Stats bar
if todos:
    pct = int((completed / total) * 100) if total else 0
    st.markdown(
        f"""
        <div style="margin-bottom:1rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem;">
                <span style="font-size:0.72rem;font-weight:600;text-transform:uppercase;
                             letter-spacing:0.08em;color:#64748b;">Progress</span>
                <span style="font-size:0.72rem;color:#64748b;font-family:monospace;">
                    {completed}/{total} done
                </span>
            </div>
            <div style="height:3px;background:rgba(255,255,255,0.06);border-radius:99px;overflow:hidden;">
                <div style="width:{pct}%;height:100%;
                            background:linear-gradient(90deg,#4f8ef7,#2dd4a0);
                            border-radius:99px;transition:width 0.4s ease;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

filter_col, _ = st.columns([2, 4])
with filter_col:
    show = st.radio("Filter", ["All", "Pending", "Done"], horizontal=True)

st.markdown('<div style="height:0.25rem;"></div>', unsafe_allow_html=True)

filtered = todos
if show == "Pending":
    filtered = [t for t in todos if t.get("status") != "COMPLETED"]
elif show == "Done":
    filtered = [t for t in todos if t.get("status") == "COMPLETED"]

if not filtered:
    if show == "All":
        empty_state("✅", "No todos yet", "Add one above or say it with Voice AI.")
    elif show == "Pending":
        empty_state("✅", "All caught up", "No pending tasks — great work.")
    else:
        empty_state("✅", "Nothing done yet", "Complete a task to see it here.")
else:
    high_todos = [t for t in filtered if (t.get("priority") or "MEDIUM").upper() == "HIGH"]
    medium_todos = [t for t in filtered if (t.get("priority") or "MEDIUM").upper() == "MEDIUM"]
    low_todos = [t for t in filtered if (t.get("priority") or "MEDIUM").upper() == "LOW"]

    if high_todos:
        st.markdown('<h3 style="font-size:1.1rem;color:#f56565;margin:1rem 0 0.5rem 0;font-weight:600;">🔴 High Priority</h3>', unsafe_allow_html=True)
        for todo in high_todos:
            todo_card(todo, on_delete=delete_todo, on_toggle=toggle_todo, on_priority_change=update_todo_priority)

    if medium_todos:
        st.markdown('<h3 style="font-size:1.1rem;color:#4f8ef7;margin:1rem 0 0.5rem 0;font-weight:600;">🔵 Medium Priority</h3>', unsafe_allow_html=True)
        for todo in medium_todos:
            todo_card(todo, on_delete=delete_todo, on_toggle=toggle_todo, on_priority_change=update_todo_priority)

    if low_todos:
        st.markdown('<h3 style="font-size:1.1rem;color:#64748b;margin:1rem 0 0.5rem 0;font-weight:600;">⚪ Low Priority</h3>', unsafe_allow_html=True)
        for todo in low_todos:
            todo_card(todo, on_delete=delete_todo, on_toggle=toggle_todo, on_priority_change=update_todo_priority)