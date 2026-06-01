import pytest
from httpx import AsyncClient
from app.services.ai.voice_parser import VoiceCommandService


def test_voice_command_service():
    # 1. Test create command intent
    res_add = VoiceCommandService.parse("add a new item")
    assert res_add["intent"] == "create"
    assert res_add["params"]["text"] == "add a new item"
    
    # 2. Test delete command intent
    res_delete = VoiceCommandService.parse("delete task #3")
    assert res_delete["intent"] == "delete"
    assert res_delete["params"]["text"] == "delete task #3"
    
    # 3. Test unknown command intent
    res_unknown = VoiceCommandService.parse("hello can you help me")
    assert res_unknown["intent"] == "unknown"
    assert res_unknown["params"] == {}


@pytest.mark.asyncio
async def test_voice_command_endpoint(client: AsyncClient):
    req_payload = {
        "text": "add groceries"
    }
    response = await client.post("/voice-command", json=req_payload)
    assert response.status_code == 200
    
    resp_json = response.json()
    assert resp_json["intent"] == "create"
    assert resp_json["parameters"]["text"] == "add groceries"
