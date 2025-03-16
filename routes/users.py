from fastapi import APIRouter, HTTPException
from models import User

router = APIRouter()

@router.get("/users/{user_id}")
async def read_user(user_id: int):
    """Возвращает информацию о пользователе по его ID."""
    # TODO: Получить пользователя из базы данных по user_id
    if not user_exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    user = User(id=user_id, name="John Doe", email="john.doe@example.com", role="user")
    return user

@router.post("/users/")
async def create_user(user: User):
    """Создает нового пользователя"""
    # TODO: Сохранить пользователя в базу данных
    return user

def user_exists(user_id: int) -> bool:
    """Заглушка для проверки существования пользователя"""
    return False