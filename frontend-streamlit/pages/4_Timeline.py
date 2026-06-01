import streamlit as st

from utils.api import get_timeline
from utils.datetime_helpers import format_local_display
from utils.layout import empty_state, load_styles, page_header, require_auth, render_sidebar

st.set_page_config(page_title="Timeline · VoiceNote AI", page_icon="📅", layout="wide")
load_styles()
render_sidebar()
require_auth()

page_header("Timeline", "Everything you've created, newest first.", "📅")

timeline = get_timeline()

if not timeline:
    empty_state("📅", "Timeline is empty", "Notes, todos, and reminders will appear here as you create them.")
else:
    # Type filter
    filter_col, _ = st.columns([2, 4])
    with filter_col:
        show = st.radio("Show", ["All", "Notes", "Todos", "Reminders"], horizontal=True)

    filtered = timeline
    if show == "Notes":
        filtered = [i for i in timeline if i.get("item_type") == "note"]
    elif show == "Todos":
        filtered = [i for i in timeline if i.get("item_type") == "todo"]
    elif show == "Reminders":
        filtered = [i for i in timeline if i.get("item_type") == "reminder"]

    if not filtered:
        empty_state("🔍", "Nothing here", f"No {show.lower()} found in the timeline.")
    else:
        st.markdown(
            f'<div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;'
            f'letter-spacing:0.1em;color:#3d4e68;margin-bottom:0.75rem;">'
            f'{len(filtered)} item{"s" if len(filtered)!=1 else ""}</div>',
            unsafe_allow_html=True,
        )
        for item in filtered:
            item_type = item.get("item_type", "note")

            type_labels = {
                "note":     ("📝", "Note",     "#4f8ef7"),
                "todo":     ("✅", "Todo",     "#2dd4a0"),
                "reminder": ("⏰", "Reminder", "#f0b429"),
            }
            icon, label, color = type_labels.get(item_type, ("·", item_type.title(), "#64748b"))

            if item_type == "note":
                body = item.get("content", "")
            elif item_type == "todo":
                body = item.get("title", "")
                status = item.get("status", "")
                if status:
                    body = f"{body}"
                    status_html = (
                        f'<span style="font-size:0.68rem;font-weight:600;'
                        f'color:{"#2dd4a0" if status=="COMPLETED" else "#f0b429"};'
                        f'text-transform:uppercase;letter-spacing:0.06em;margin-left:0.5rem;">'
                        f'{status.lower()}</span>'
                    )
                else:
                    status_html = ""
            else:
                body = format_local_display(item.get("reminder_time", ""))
                status_html = ""

            meta_raw = item.get("created_at") or item.get("reminder_time") or ""
            meta = format_local_display(meta_raw) if meta_raw else ""

            st.markdown(
                f"""
                <div style="
                    display:flex;align-items:flex-start;gap:1rem;
                    padding:0.85rem 0;
                    border-bottom:1px solid rgba(255,255,255,0.04);
                ">
                    <div style="
                        display:flex;flex-direction:column;align-items:center;
                        padding-top:4px;flex-shrink:0;
                    ">
                        <div style="
                            width:8px;height:8px;border-radius:50%;
                            background:{color};
                            box-shadow:0 0 8px {color}88;
                            flex-shrink:0;
                        "></div>
                    </div>
                    <div style="flex:1;min-width:0;">
                        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.25rem;">
                            <span style="font-size:0.68rem;font-weight:700;text-transform:uppercase;
                                         letter-spacing:0.1em;color:{color};">{label}</span>
                            {"" if item_type != "todo" or not item.get("status") else status_html}
                        </div>
                        <div style="font-size:0.88rem;color:#aab4c8;font-weight:300;
                                    line-height:1.5;word-break:break-word;">
                            {body[:200]}{"…" if len(str(body)) > 200 else ""}
                        </div>
                        <div style="font-size:0.7rem;color:#3d4e68;margin-top:0.3rem;
                                    font-family:monospace;letter-spacing:0.02em;">{meta}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )