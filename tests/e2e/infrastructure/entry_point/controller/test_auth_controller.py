"""E2E tests for authentication controller"""
import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.e2e
class TestAuthController:
    """E2E tests for authentication endpoints"""
    
    @pytest.mark.asyncio
    async def test_register_success(self):
        """Test successful user registration"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/auth/register",
                json={
                    "id": "9876543210",
                    "name": "New",
                    "lastName": "User",
                    "email": "newuser@example.com",
                    "password": "password123"
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["email"] == "newuser@example.com"
            assert data["name"] == "New"
            assert "token" not in data  # Token not returned on registration
    
    @pytest.mark.asyncio
    async def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/auth/login",
                json={
                    "email": "wrong@example.com",
                    "password": "wrongpassword"
                }
            )
            
            assert response.status_code == 401
            data = response.json()
            assert data["success"] is False
            assert "error" in data
