from pydantic import BaseModel, Field, EmailStr


class NewMember(BaseModel):
    user_email: EmailStr
    project_id: int


class AssignRole(BaseModel):
    project_id: int
    user_id: int
    role_id: int


class RemoveMember(BaseModel):
    project_id: int
    user_id: int