import pytest
from unittest.mock import MagicMock
from app.services.ai.transcription import TranscriptionService


def test_transcription_service(mocker):
    # Mock get_model to return a mock model and keep tests offline-friendly and instant
    mock_model = MagicMock()
    mock_model.transcribe.return_value = {
        "text": "Hello world, this is a test voice capture.",
        "language": "en",
        "segments": [
            {"id": 0, "start": 0.0, "end": 2.0, "text": "Hello world"},
            {"id": 1, "start": 2.0, "end": 4.0, "text": "this is a test"}
        ]
    }
    mocker.patch("app.services.ai.transcription.get_model", return_value=mock_model)

    result = TranscriptionService.transcribe("dummy_voice.wav")
    
    # Verify underlying call and payload
    mock_model.transcribe.assert_called_once_with("dummy_voice.wav")
    assert result["text"] == "Hello world, this is a test voice capture."
    assert result["language"] == "en"
    assert len(result["segments"]) == 2
