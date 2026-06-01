import pytest
from httpx import AsyncClient
from app.services.ai.classification import ClassificationService


def test_classification_service_predict():
    # Test service direct inference on various text inputs
    res_todo = ClassificationService.classify("Buy groceries tomorrow")
    assert res_todo["label"] in ["todo", "reminder", "note"]
    assert isinstance(res_todo["confidence"], float)
    assert 0.0 <= res_todo["confidence"] <= 1.0
    assert "note" in res_todo["scores"]
    assert "todo" in res_todo["scores"]
    assert "reminder" in res_todo["scores"]

    res_note = ClassificationService.classify("This is just an idea for future reference")
    assert res_note["label"] in ["todo", "reminder", "note"]
    assert isinstance(res_note["confidence"], float)


@pytest.mark.asyncio
async def test_classify_endpoint(client: AsyncClient):
    # Test POST /classify endpoint
    req_payload = {
        "text": "Meeting with John at 2 PM next Friday"
    }
    response = await client.post("/classify", json=req_payload)
    assert response.status_code == 200
    
    resp_json = response.json()
    assert "label" in resp_json
    assert "confidence" in resp_json
    assert isinstance(resp_json["confidence"], float)
    assert resp_json["label"] in ["note", "todo", "reminder"]
