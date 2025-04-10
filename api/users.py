from fastapi import APIRouter, HTTPException
from models.queries.orm import AsyncORM
from schemes.users import User, NewUser


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", summary="Get all users")
async def get_users() -> list[User]:
    res = await AsyncORM.select_users()
    if not res:
        raise HTTPException(status_code=404, detail="Users not found")
    return res 

@router.get("/{id}", summary="Get user by id")
async def get_user_by_id(user_id: int) -> User:
    users = await AsyncORM.select_users()
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/", summary="Post user")
async def create_user(new_user: NewUser) -> int:
    user = {
        "username": new_user.username,
        "password": new_user.password,
        "email": new_user.email
    }
    
    user_id = await AsyncORM.insert_user(user)
    return user_id
    
    