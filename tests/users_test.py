import pytest
from fastapi import status
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch

from backend.main import app
from backend.api.security.security import security
from backend.schemes.users import User


@pytest.mark.asyncio
async def test_successful_login():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
    
        test_credentials = {
            "email": "andrew@mail.ru",
            "password": "hash1"
        }

        with patch(
            "backend.api.users.login", new_callable=AsyncMock
        ) as mock_auth, patch(
            "backend.api.security.security.security.create_access_token"
        ) as mock_token:
            
            mock_token.return_value = "mocked_jwt_token"

            response = await client.post(
                "/users/login",
                json=test_credentials
            )

            assert response.status_code == status.HTTP_200_OK
            assert response.json() == {"access_token": "mocked_jwt_token"}

            cookies = response.cookies
            assert "my_access_token" in cookies
            assert cookies["my_access_token"] == "mocked_jwt_token"

            security.create_access_token.assert_called_once()  # type: ignore


@pytest.mark.asyncio
async def test_login_user_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        invalid_credentials = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }

        with patch(
            "backend.api.users.AsyncORM.authenticate_user",
            new_callable=AsyncMock,
            return_value=None
        ):
            response = await client.post(
                "/users/login",
                json=invalid_credentials
            )

            assert response.status_code == status.HTTP_401_UNAUTHORIZED
            assert response.json() == {"detail": "Incorrect username or password"}
            
            assert "my_access_token" not in response.cookies

@pytest.mark.asyncio
async def test_get_existing_user():
    """Тест успешного получения существующего пользователя"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Создаем тестового пользователя, соответствующего вашей модели
        test_user = User(
            id=1,
            username="andrew",  # Должно совпадать с ожидаемым значением
            email="andrew@mail.ru",
            password="hash1"
        )

        # 2. Мокируем ORM
        with patch(
            "backend.api.users.AsyncORM.select_users",
            new_callable=AsyncMock,
            return_value=[test_user]
        ):
            # 3. Делаем запрос (убедитесь, что путь правильный)
            response = await client.get(f"/users/{test_user.id}")
            
            # 4. Проверяем ответ
            assert response.status_code == status.HTTP_200_OK
            
            # 5. Проверяем, что ответ содержит ТОЛЬКО ожидаемые поля
            response_data = response.json()
            assert response_data["id"] == test_user.id
            assert response_data["username"] == test_user.username
            assert response_data["email"] == test_user.email
            assert "password" not in response_data  # Пароль не должен возвращаться

@pytest.mark.asyncio
async def test_get_nonexistent_user():
    """Тест случая, когда пользователь не найден"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        with patch(
            "backend.api.users.AsyncORM.select_users",
            new_callable=AsyncMock,
            return_value=[]  # Мок возвращает пустой список
        ):
            response = await client.get("/users/999")
            
            assert response.status_code == status.HTTP_404_NOT_FOUND
            assert response.json() == {"detail": "User not found"}