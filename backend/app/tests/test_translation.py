import pytest
from httpx import AsyncClient
from app.services.ai.translation import TranslationService


def test_translation_service(mocker):
    # Mock argostranslate module's translate function directly in the library
    mock_argos_translate = mocker.patch("argostranslate.translate.translate")
    mock_argos_translate.return_value = "Bonjour le monde"

    result = TranslationService.translate("Hello world", "en", "fr")
    
    mock_argos_translate.assert_called_once_with("Hello world", "en", "fr")
    assert result == "Bonjour le monde"


@pytest.mark.asyncio
async def test_translate_endpoint(client: AsyncClient, mocker):
    # Mock TranslationService.translate to prevent hitting actual translators
    mock_service = mocker.patch("app.services.ai.translation.TranslationService.translate")
    mock_service.return_value = "Hola Mundo"
    
    req_payload = {
        "text": "Hello World",
        "source_language": "en",
        "target_language": "es"
    }
    
    response = await client.post("/translate", json=req_payload)
    assert response.status_code == 200
    
    resp_json = response.json()
    assert resp_json["translated_text"] == "Hola Mundo"
    mock_service.assert_called_once_with("Hello World", "en", "es")
