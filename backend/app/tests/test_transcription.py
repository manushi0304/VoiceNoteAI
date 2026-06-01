import pytest
from unittest.mock import MagicMock
from app.services.ai.transcription import TranscriptionService


def test_transcription_service(mocker):
    # Mock whisper model's transcribe method to keep tests offline-friendly and instant
    mock_transcribe = mocker.patch("app.services.ai.transcription._model.transcribe")
    mock_transcribe.return_value = {
        "text": "Hello world, this is a test voice capture.",
        "language": "en",
        "segments": [
            {"id": 0, "start": 0.0, "end": 2.0, "text": "Hello world"},
            {"id": 1, "start": 2.0, "end": 4.0, "text": "this is a test"}
        ]
    }

    result = TranscriptionService.transcribe("dummy_voice.wav")
    
    # Verify underlying call and payload
    mock_transcribe.assert_called_once_with("dummy_voice.wav")
    assert result["text"] == "Hello world, this is a test voice capture."
    assert result["language"] == "en"
    assert len(result["segments"]) == 2
