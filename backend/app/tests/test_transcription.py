import pytest
from unittest.mock import MagicMock
from app.services.ai.transcription import TranscriptionService


def test_transcription_service(mocker):
    # Mock get_model to return a mock model and keep tests offline-friendly and instant
    mock_model = MagicMock()
    
    mock_seg1 = MagicMock()
    mock_seg1.id = 0
    mock_seg1.start = 0.0
    mock_seg1.end = 2.0
    mock_seg1.text = "Hello world,"
    
    mock_seg2 = MagicMock()
    mock_seg2.id = 1
    mock_seg2.start = 2.0
    mock_seg2.end = 4.0
    mock_seg2.text = "this is a test voice capture."
    
    mock_info = MagicMock()
    mock_info.language = "en"
    
    mock_model.transcribe.return_value = ([mock_seg1, mock_seg2], mock_info)
    mocker.patch("app.services.ai.transcription.get_model", return_value=mock_model)

    result = TranscriptionService.transcribe("dummy_voice.wav")
    
    # Verify underlying call and payload
    mock_model.transcribe.assert_called_once_with("dummy_voice.wav", beam_size=5)
    assert result["text"] == "Hello world, this is a test voice capture."
    assert result["language"] == "en"
    assert len(result["segments"]) == 2
