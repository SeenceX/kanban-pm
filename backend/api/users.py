from fastapi import APIRouter, HTTPException, Response, Depends
from backend.models.queries.orm import AsyncORM
from backend.schemes.users import User, NewUser, UserLogin
from backend.api.security.security import security



router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/login")
async def login(credits: UserLogin, response: Response):
    # Тут сделать запрос в ORM
    email = credits.email
    password = credits.password
    user = await AsyncORM.authenticate_user(email, password)

    if not user:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password"
        )

    token = security.create_access_token(uid="12345")
    response.set_cookie(security.config.JWT_ACCESS_COOKIE_NAME, token)
    return {"access_token": token, "data": {"id": user.id, "email": user.email}}

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
    
    