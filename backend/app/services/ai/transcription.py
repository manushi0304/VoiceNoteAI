import os
import whisper

# Only append local dev ffmpeg path on Windows
if os.name == 'nt':
    os.environ["PATH"] += os.pathsep + r"C:\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin"

_model = None

def get_model():
    global _model
    if _model is None:
        model_size = os.getenv("WHISPER_MODEL_SIZE", "tiny")
        print(f"📥 Loading Whisper model '{model_size}'...")
        _model = whisper.load_model(model_size)
        print("✅ Whisper model loaded successfully!")
    return _model


class TranscriptionService:
    @staticmethod
    def transcribe(audio_path: str) -> dict:
        model = get_model()
        result = model.transcribe(audio_path)
        return {
            "text": result["text"],
            "language": result["language"],
            "segments": result["segments"],
        }

