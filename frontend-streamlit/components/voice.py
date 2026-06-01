import streamlit as st
from utils.api import post

def voice_input():
    audio = st.file_uploader("🎙️ Speak", type=["wav", "mp3"])
    if audio:
        res = post("/voice-create", files={"file": audio})
        st.success(res["transcript"])
 
