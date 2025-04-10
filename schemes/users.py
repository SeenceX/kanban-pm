from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id: int
    username: str
    email: EmailStr


class NewUser(BaseModel):
    username: str
    password: str
    email: EmailStr

