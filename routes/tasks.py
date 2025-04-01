from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, EmailStr
from schemas.queries.orm import AsyncORM

router = APIRouter(
    prefix="/tasks",
    tags=["Task"]
)


class NewTask(BaseModel):
    title: str = Field(max_length=50)
    description: str
    status: bool
    stage_id: int
    assigned_user_id: int | None


class MoveTask(BaseModel):
    stage_id: int


class TaskDescriptionUpdate(BaseModel):
    description: str


class TaskExecutor(BaseModel):
    task_id: int


@router.get("/stage/{stage_id}", summary="Get all task of a stage by stage_id")
async def get_tasks_by_stage_id(stage_id: int):
    tasks = await AsyncORM.get_tasks_by_stage_id(stage_id)

    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")

    return tasks

@router.get("/project/{project_id}", summary="Get all tasks of a project by project_id")
async def get_tasks_by_project_id(project_id: int):
    tasks = await AsyncORM.get_tasks_by_project_id(project_id)

    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")

    return tasks

@router.post("/", tags=["ToDo"], summary="Create a new task")
async def create_task(task_data: NewTask):
    pass

@router.patch("/{task_id}", tags=["ToDo"], summary="Move task to another stage")
async def move_task(task_id: int, stage_id: MoveTask):
    pass

@router.delete("/{task_id}", tags=["ToDo"], summary="Remove a task by id")
async def remove_task(task_id: int):
    pass

@router.patch("/{task_id}/description", tags=["ToDo"], summary="Update the description of the task")
async def update_description(task_id: int, update_data: TaskDescriptionUpdate):
    pass

@router.patch("/executor/{user_id}", tags=["ToDo"], summary="Accept task")
async def assign_to(user_id: int, assign_data: TaskExecutor):
    pass

@router.patch("/{task_id}/status", tags=["ToDo"], summary="Change the status of the task")
async def change_status(task_id: int):
    pass

@router.get("/{task_id}/comments", tags=["ToDo"], summary="Get the comments on the task")
async def get_comments(task_id: int):
    pass