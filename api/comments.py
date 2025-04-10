from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, EmailStr
from models.queries.orm import AsyncORM

router = APIRouter(
    prefix="/tasks/comments",
    tags=["Comments"]
)


class NewComment(BaseModel):
    text: str = Field(max_length=256)
    task_id: int
    author_id: int


@router.post("/", summary="Create the comment")
async def create_comment(new_comment: NewComment):
    data = {
        "text": new_comment.text,
        "task_id": new_comment.task_id,
        "author_id": new_comment.author_id
    }

    await AsyncORM.create_comment(data)

@router.delete("/{comment_id}", summary="Remove the comments on task")
async def remove_comment(comment_id: int):
    await AsyncORM.remove_comment(comment_id)
