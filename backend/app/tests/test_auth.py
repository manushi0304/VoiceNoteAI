import pytest
import uuid
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.services.auth_service import AuthService
from app.schemas.auth import UserCreate

@pytest.mark.asyncio
async def test_auth_service_register_and_authenticate(db_session: AsyncSession):
    unique_email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    
    # 1. Test registration
    user_in = UserCreate(
        email=unique_email,
        password="securepassword",
        full_name="Test User"
    )
    result = await AuthService.register(db_session, user_in)
    assert result["email"] == unique_email
    assert "id" in result

    # 2. Test duplicate registration (should raise 400)
    with pytest.raises(HTTPException) as exc_info:
        await AuthService.register(db_session, user_in)
    assert exc_info.value.status_code == 400
    assert "Email already registered" in exc_info.value.detail

    # 3. Test authentication success
    user = await AuthService.authenticate(
        db_session,
        email=unique_email,
        password="securepassword"
    )
    assert user is not None
    assert user.email == unique_email

    # 4. Test authentication fail - wrong password
    user_wrong_pass = await AuthService.authenticate(
        db_session,
        email=unique_email,
        password="wrongpassword"
    )
    assert user_wrong_pass is None

    # 5. Test authentication fail - wrong email
    user_wrong_email = await AuthService.authenticate(
        db_session,
        email=f"wrong_{unique_email}",
        password="securepassword"
    )
    assert user_wrong_email is None


@pytest.mark.asyncio
async def test_auth_endpoints(client: AsyncClient):
    unique_email = f"endpoint_{uuid.uuid4().hex[:8]}@example.com"
    
    # 1. Test POST /auth/register
    reg_data = {
        "email": unique_email,
        "password": "endpointpassword",
        "full_name": "Endpoint User"
    }
    response = await client.post("/auth/register", json=reg_data)
    assert response.status_code == 200
    assert response.json()["email"] == unique_email

    # 2. Test POST /auth/login success
    login_data = {
        "username": unique_email,
        "password": "endpointpassword"
    }
    response = await client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    token_json = response.json()
    assert "access_token" in token_json
    assert token_json["token_type"] == "bearer"

    # 3. Test POST /auth/login failure
    bad_login_data = {
        "username": unique_email,
        "password": "wrongpassword"
    }
    response = await client.post("/auth/login", data=bad_login_data)
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]
