from fastapi import APIRouter, HTTPException, Response, Depends
from backend.models.queries.orm import AsyncORM
from backend.schemes.users import User, NewUser, UserLogin
from backend.api.security.security import security
from datetime import timedelta



router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/login")
async def login(credits: UserLogin, response: Response):

    email = credits.email
    password = credits.password
    user = await AsyncORM.authenticate_user(email, password)

    if not user:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password"
        )

    access_token = security.create_access_token(
        uid=str(user.id),
        data={
            "email": user.email,
            "username": user.username
        },
        expires_delta=timedelta(minutes=10)
    )

    security.set_access_cookies(access_token, response)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username
        }
    }


@router.get("/", summary="Get all users", dependencies=[Depends(security.access_token_required)])
async def get_users() -> list[User]:
    res = await AsyncORM.select_users()
    if not res:
        raise HTTPException(status_code=404, detail="Users not found")
    return res 

@router.get("/{id}", summary="Get user by id")
async def get_user_by_id(id: int) -> User:
    users = await AsyncORM.select_users()
    for user in users:
        if user.id == id:
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
    
    