from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, EmailStr
from schemas.queries.orm import AsyncORM

# router = APIRouter(
#     prefix="/tasks/comments",
#     tags=["Task"]
# )

# TODO: Продумать какой будет тут префикс


class CommentToRemove(BaseModel):
    comment_id: int


@router.delete("/task/{task_id}/comments", tags=["ToDo"], summary="Remove the comments on task")
async def remove_comment(task_id: int, remove_data: CommentToRemove):
    pass
