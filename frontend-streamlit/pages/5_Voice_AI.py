import tempfile

import requests
import streamlit as st
from streamlit_mic_recorder import mic_recorder

from utils.layout import load_styles, page_header, require_auth, render_sidebar

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Voice AI · VoiceNote AI", page_icon="🎤", layout="wide")
load_styles()
render_sidebar()
require_auth()

page_header(
    "Voice AI",
    "Record once — AI transcribes, classifies, and creates the right item automatically.",
    "🎤",
)

st.markdown(
    """
    <div class="voice-card">
        <h1>Hands-free capture</h1>
        <p>
            Say things like <em>"remind me to call mom at 8pm"</em> or <em>"buy milk tomorrow"</em>.
            The assistant picks note, todo, or reminder for you — no typing needed.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("Tips for best results"):
    st.markdown(
        """
        - Speak clearly for **3–10 seconds** for best accuracy
        - Include a time reference for reminders: *"at 6pm"*, *"tomorrow morning"*
        - Keep the backend running on port **8000**
        - Reduce background noise if transcription quality is low
        """
    )

st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)

audio = mic_recorder(
    start_prompt="⏺  Start recording",
    stop_prompt="⏹  Stop & process",
    just_once=True,
    use_container_width=True,
)

if audio:
    st.audio(audio["bytes"], format="audio/wav")
    st.markdown('<div style="height:0.35rem;"></div>', unsafe_allow_html=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio["bytes"])
        audio_path = tmp.name

    headers = {"Authorization": f"Bearer {st.session_state['token']}"}

    with st.spinner("Transcribing and classifying…"):
        with open(audio_path, "rb") as f:
            response = requests.post(
                f"{API_BASE}/voice-create/",
                headers=headers,
                files={"file": f},
            )

    if response.status_code == 200:
        data = response.json()
        item_type = data.get("type", "—").title()
        conf      = float(data.get("confidence", 0))
        conf_pct  = f"{conf * 100:.0f}%"

        st.success("Done — item created from your voice.")
        st.markdown('<div style="height:0.25rem;"></div>', unsafe_allow_html=True)

        # Result summary card
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f'<div style="padding:1rem 1.1rem;background:rgba(255,255,255,0.03);'
                f'border:1px solid rgba(255,255,255,0.08);border-radius:8px;">'
                f'<div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;'
                f'letter-spacing:0.1em;color:#64748b;margin-bottom:0.4rem;">Type</div>'
                f'<div style="font-size:1.15rem;font-weight:600;color:#e8edf5;">{item_type}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with c2:
            conf_color = "#2dd4a0" if conf >= 0.8 else "#f0b429" if conf >= 0.5 else "#f56565"
            st.markdown(
                f'<div style="padding:1rem 1.1rem;background:rgba(255,255,255,0.03);'
                f'border:1px solid rgba(255,255,255,0.08);border-radius:8px;">'
                f'<div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;'
                f'letter-spacing:0.1em;color:#64748b;margin-bottom:0.4rem;">Confidence</div>'
                f'<div style="font-size:1.15rem;font-weight:600;color:{conf_color};">{conf_pct}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with c3:
            if data.get("reminder_time"):
                from utils.datetime_helpers import format_local_display
                sched = format_local_display(data["reminder_time"])
                st.markdown(
                    f'<div style="padding:1rem 1.1rem;background:rgba(255,255,255,0.03);'
                    f'border:1px solid rgba(255,255,255,0.08);border-radius:8px;">'
                    f'<div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;'
                    f'letter-spacing:0.1em;color:#64748b;margin-bottom:0.4rem;">Scheduled</div>'
                    f'<div style="font-size:0.88rem;font-weight:500;color:#e8edf5;">{sched}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div style="padding:1rem 1.1rem;background:rgba(255,255,255,0.03);'
                    'border:1px solid rgba(255,255,255,0.08);border-radius:8px;'
                    'display:flex;align-items:center;justify-content:center;">',
                    unsafe_allow_html=True,
                )
                st.page_link("pages/4_Timeline.py", label="View in Timeline →", icon="📅")
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)

        st.markdown(
            '<div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;'
            'letter-spacing:0.1em;color:#3d4e68;margin-bottom:0.5rem;">Transcript</div>',
            unsafe_allow_html=True,
        )
        st.info(data.get("transcript", ""))

        st.markdown('<div style="height:0.35rem;"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size:0.68rem;color:#3d4e68;margin-bottom:0.3rem;'
            'font-family:monospace;">Confidence</div>',
            unsafe_allow_html=True,
        )
        st.progress(min(conf, 1.0))

    else:
        st.error("Voice processing failed. Check the backend logs.")
        try:
            st.json(response.json())
        except Exception:
            st.code(response.text)