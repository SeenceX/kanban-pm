from fastapi import APIRouter, HTTPException
from models.queries.orm import AsyncORM
from schemes.tasks import Task, NewTask, MoveTask, TaskDescriptionUpdate, TaskExecutor, TaskComments


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.get("/stage/{stage_id}", summary="Get all task of a stage by stage_id")
async def get_tasks_by_stage_id(stage_id: int) -> list[Task]:
    tasks = await AsyncORM.get_tasks_by_stage_id(stage_id)

    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")

    return tasks

@router.get("/project/{project_id}", summary="Get all tasks of a project by project_id")
async def get_tasks_by_project_id(project_id: int) -> list[Task]:
    tasks = await AsyncORM.get_tasks_by_project_id(project_id)

    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")

    return tasks

@router.post("/", summary="Create a new task")
async def create_task(task_data: NewTask):
    data = {
        "title": task_data.title,
        "description": task_data.description,
        "status": task_data.status,
        "stage_id": task_data.stage_id,
        "creator_id": task_data.creator_id,
        "assigned_user_id": task_data.assigned_user_id
    }
    await AsyncORM.create_task(data)

# TODO: Здесь нужно будет дописать проверку на существование Stage
@router.patch("/{task_id}", summary="Move task to another stage")
async def move_task(task_id: int, stage_id: MoveTask):
    data = {
        "stage_id": stage_id.stage_id,
        "task_id": task_id
    }

    await AsyncORM.move_task(data)

@router.delete("/{task_id}", summary="Remove a task by id")
async def remove_task(task_id: int):
    return await AsyncORM.delete_task(task_id)

#TODO: Дописать проверку на существование Task
@router.patch("/{task_id}/description", summary="Update the description of the task")
async def update_description(task_id: int, update_data: TaskDescriptionUpdate):
    await AsyncORM.update_description(task_id, update_data.description)

#TODO: Дописать проверку на существование Task и User
@router.patch("/executor/{user_id}", summary="Accept task")
async def assign_to(user_id: int, assign_data: TaskExecutor):
    await AsyncORM.assing_to(assign_data.task_id, user_id)

#TODO: Проверку на существование Task
@router.patch("/{task_id}/status", summary="Change the status of the task")
async def change_status(task_id: int):
    await AsyncORM.set_status(task_id)

#TODO: Проверку на существование Task
@router.get("/{task_id}/comments", summary="Get the comments on the task")
async def get_comments(task_id: int) -> list[TaskComments]:
    result = await AsyncORM.get_comments(task_id)

    if not result:
        raise HTTPException(status_code=404, detail="There are no comments")
    
    return result