from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class Task(BaseModel):
    id: int
    title: str
    status: bool
    description: str
    stage_id: int
    creator_id: int
    assigned_user_id: int | None


class NewTask(BaseModel):
    title: str = Field(max_length=50)
    description: str
    status: bool
    stage_id: int
    creator_id: int
    assigned_user_id: int | None


class MoveTask(BaseModel):
    stage_id: int


class TaskDescriptionUpdate(BaseModel):
    description: str


class TaskExecutor(BaseModel):
    task_id: int


class TaskComments(BaseModel):
    id: int
    text: str
    author_id: int
    created_at: datetime
    task_id: int