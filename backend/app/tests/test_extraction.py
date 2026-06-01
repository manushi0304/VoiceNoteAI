import pytest
from httpx import AsyncClient
from app.services.ai.extraction import ExtractionService


def test_extraction_service():
    # 1. Test PERSON entity extraction
    text = "Call John Miller tomorrow morning"
    res = ExtractionService.extract(text)
    assert isinstance(res["people"], list)
    assert any("John" in person for person in res["people"])
    
    # 2. Test DATE/TIME entity extraction
    assert isinstance(res["dates"], list)
    assert len(res["dates"]) >= 1
    assert any("tomorrow" in dt.lower() for dt in res["dates"])
    assert res["priority"] == "MEDIUM"


@pytest.mark.asyncio
async def test_extract_entities_endpoint(client: AsyncClient):
    req_payload = {
        "text": "Email Sarah Smith next Monday regarding the budget"
    }
    response = await client.post("/extract-entities", json=req_payload)
    assert response.status_code == 200
    
    resp_json = response.json()
    assert "people" in resp_json
    assert "dates" in resp_json
    assert "priority" in resp_json
    assert any("Sarah" in p for p in resp_json["people"])
    assert len(resp_json["dates"]) >= 1
