import streamlit as st

from components.cards import note_card
from utils.api import create_note, delete_note, get_notes
from utils.layout import empty_state, load_styles, page_header, require_auth, render_sidebar

st.set_page_config(page_title="Notes · VoiceNote AI", page_icon="📝", layout="wide")
load_styles()
render_sidebar()
require_auth()

page_header("Notes", "Capture ideas, references, and meeting takeaways.", "📝")

with st.form("new_note", clear_on_submit=True):
    note_text = st.text_area(
        "New note",
        placeholder="Start writing — meeting takeaways, ideas, links…",
        height=110,
    )
    submitted = st.form_submit_button("Save note →", type="primary", use_container_width=True)

if submitted:
    if note_text.strip():
        if create_note(note_text):
            st.success("Note saved.")
            st.rerun()
        else:
            st.error("Could not save. Check that the API is running on port 8000.")
    else:
        st.warning("Write something before saving.")

st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)

notes = get_notes()

# Count label
if notes:
    st.markdown(
        f'<div style="display:flex;align-items:center;justify-content:space-between;'
        f'margin-bottom:0.9rem;">'
        f'<span style="font-size:0.7rem;font-weight:700;text-transform:uppercase;'
        f'letter-spacing:0.1em;color:#3d4e68;">{len(notes)} note{"s" if len(notes)!=1 else ""}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
    for note in notes:
        note_card(note, on_delete=delete_note)
else:
    empty_state("📝", "No notes yet", "Save a note above or use Voice AI to create one hands-free.")