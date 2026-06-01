import os
import whisper

os.environ["PATH"] += os.pathsep + r"C:\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin"

_model = whisper.load_model("base")


class TranscriptionService:
    @staticmethod
    def transcribe(audio_path: str) -> dict:
        result = _model.transcribe(audio_path)
        return {
            "text": result["text"],
            "language": result["language"],
            "segments": result["segments"],
        }
