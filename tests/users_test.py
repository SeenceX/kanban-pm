import pytest
from fastapi import status
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch

from backend.main import app
from backend.api.security.security import security

@pytest.fixture
async def async_client():
    """Фикстура для создания асинхронного тестового клиента."""
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        yield client

@pytest.mark.asyncio
async def test_login_success(async_client):
    """Тест успешной аутентификации пользователя."""
    # Мокируем метод аутентификации
    with patch("backend.api.users.authenticate_user", new_callable=AsyncMock) as mock_auth:
        mock_auth.return_value = {"id": "1", "email": "andrew@mail.ru"}  # Возвращаем мок пользователя

        test_credentials = {
            "email": "andrew@mail.ru",
            "password": "hash1"
        }

        # Отправляем запрос на вход
        response = await async_client.post(
            "/login",
            json=test_credentials,
            headers={"Content-Type": "application/json"}
        )
        
        # Проверяем ответ
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "access_token" in response_data
        assert isinstance(response_data["access_token"], str)
        
        # Проверяем установку cookie
        cookies = response.cookies
        assert security.config.JWT_ACCESS_COOKIE_NAME in cookies
        assert cookies[security.config.JWT_ACCESS_COOKIE_NAME] is not None

@pytest.mark.asyncio
async def test_login_failure(async_client):
    """Тест неудачной аутентификации."""
    with patch("backend.api.users.authenticate_user", new_callable=AsyncMock) as mock_auth:
        mock_auth.return_value = None  # Пользователь не найден

        response = await async_client.post(
            "/login",
            json={"email": "wrong@mail.ru", "password": "wrongpass"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Incorrect username or password"