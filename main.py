from fastapi import FastAPI, HTTPException, status
#from routes import users
import uvicorn
from schemas.queries.orm import AsyncORM
from pydantic import BaseModel, EmailStr, Field
import asyncio

app = FastAPI(
    title="Kanban project management",
    description="API для управления системой",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Users",
            "description": "Операции с пользователями"
        },
        {
            "name": "Project",
            "description": "Операции с проектами"
        },
        {
            "name": "Project members",
            "description": "Управление участниками проекта"
        },
        {
            "name": "Project stages",
            "description": "Операции с этапами проекта"
        },
        {
            "name": "Task",
            "description": "Операции с задачами"
        }
    ]
)


#app.include_router(users.router)
# uvicorn app:app


@app.get("/users", tags=["Users"], summary="Get all users")
async def get_users():
    return await AsyncORM.select_users()

@app.get("/users/{id}", tags=["Users"], summary="Get user by id")
async def get_user_by_id(user_id: int):
    users = await AsyncORM.select_users()
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


class NewUser(BaseModel):
    username: str
    password: str
    email: EmailStr


@app.post("/users", tags=["Users"], summary="Post user")
async def create_user(new_user: NewUser):
    user = {
        "username": new_user.username,
        "password": new_user.password,
        "email": new_user.email
    }
    
    await AsyncORM.insert_user(user)


@app.get("/projects", tags=["Project"], summary="Get all projects")
async def get_projects():
    return await AsyncORM.select_projects()

@app.get("/project/{creator_id}", tags=["Project"], summary="Get project by creator id")
async def get_projects_by_creator_id(creator_id: int):
    projects = await AsyncORM.select_projects()
    result = []
    for project in projects:
        if project.creator_id == creator_id:
            result.append(project)
    
    if len(result) > 0:
        return result
    else:
        raise HTTPException(status_code=404, detail="Projects not found")


class NewProject(BaseModel):
    title: str = Field(max_length=50)
    creator_id: int

@app.post("/project", tags=["Project"], summary="Post project")
async def create_project(new_project: NewProject):
    project = {
        "title": new_project.title,
        "creator_id": new_project.creator_id
    }

    await AsyncORM.create_project(project)


class NewMember(BaseModel):
    user_email: EmailStr
    project_id: int

@app.post("/project/members/add", tags=["Project members"], summary="Add member to project")
async def add_member(new_member: NewMember):
    data = {
        "email": new_member.user_email,
        "project_id": new_member.project_id,
    }

    is_finded = False
    users = await AsyncORM.select_users()
    for user in users:
        if user.email == data["email"]:
            data["user_id"] = user.id
            is_finded = True
    
    if not is_finded:
        raise HTTPException(status_code=404, detail="User not found")
    
    await AsyncORM.add_member(data)
    
    print(data)


class RemoveMember(BaseModel):
    project_id: int
    user_id: int

@app.delete("/project/members/remove", tags=["Project members"], summary="Remove a member from project")
async def remove_member(remove_member_data: RemoveMember):
    data = {
        "project_id": remove_member_data.project_id,
        "user_id": remove_member_data.user_id
    }
    return await AsyncORM.remove_member(data)


class AssignRole(BaseModel):
    project_id: int
    user_id: int
    role_id: int
    
@app.put("/project/members/assign_role", tags=["Project members"], summary="Assign role to member")
async def assign_role(assign_member_role_date: AssignRole):
    data = {
        "project_id": assign_member_role_date.project_id,
        "user_id": assign_member_role_date.user_id,
        "role_id": assign_member_role_date.role_id
    }
    
    result = await AsyncORM.assign_role(data)

    if not result:
        raise HTTPException(status_code=404, detail="Membership not found")
    
    return {"status": "success", "message": "Role updated"}


class NewStage(BaseModel):
    name: str
    project_id: int

@app.post("/project/create_stage", tags=["Project stages"], summary="Add stage to project")
async def create_stage(stage_data: NewStage):
    data = {
        "name": stage_data.name,
        "project_id": stage_data.project_id
    }
    return await AsyncORM.create_stage(data)


class RemoveStage(BaseModel):
    stage_id: int
    project_id: int

@app.delete("/project/remove_stage", tags=["Project stages"], summary="Remove a stage from project")
async def create_stage(remove_stage_data: RemoveStage):
    data = {
        "stage_id": remove_stage_data.stage_id,
        "project_id": remove_stage_data.project_id
    }
    await AsyncORM.remove_stage(data)
    await AsyncORM.reorder_stages(data["project_id"])



@app.get("/reorder_project_stages", tags=["Project stages"], summary="Пересчет порядка этапов", deprecated=True)
async def reorder_stages(project_id: int):
    await AsyncORM.reorder_stages(project_id)


class MoveStage(BaseModel):
    new_position: int = Field(..., gt=0, description="Новая позиция (начиная с 1)")

@app.patch("/project/{stage_id}/move_stage", tags=["Project stages"], summary="Move a stage")
async def move_stage(stage_id: int, move_stage_data: MoveStage):

    data = {
        "new_position": move_stage_data.new_position
    }

    result = await AsyncORM.move_stage(stage_id, data)

    if not result:
        raise HTTPException(status_code=404, detail="Stage not found or invalid position")
    
    return {"status": "success", "message": "Stage position updated"}


@app.get("/project/stages/{project_id}", tags=["Project stages"], summary="Get all stages of a project")
async def get_stages(project_id: int):
    return await AsyncORM.get_stages(project_id)


@app.patch("/project/stages/limit/", tags=["ToDo"], summary="set the limit on the stage")
async def set_limit():
    pass


@app.get("/tasks/stage/{stage_id}", tags=["Task"], summary="Get all task of a stage by stage_id")
async def get_tasks_by_stage_id(stage_id: int):
    tasks = await AsyncORM.get_tasks_by_stage_id(stage_id)

    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")

    return tasks

@app.get("/tasks/project/{project_id}", tags=["Task"], summary="Get all tasks of a project by project_id")
async def get_tasks_by_project_id(project_id: int):
    tasks = await AsyncORM.get_tasks_by_project_id(project_id)

    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")

    return tasks


class NewTask(BaseModel):
    title: str = Field(max_length=50)
    description: str
    status: bool
    stage_id: int
    assigned_user_id: int | None

@app.post("/task", tags=["ToDo"], summary="Create a new task")
async def create_task(task_data: NewTask):
    pass


class MoveTask(BaseModel):
    stage_id: int

@app.patch("/task/{task_id}", tags=["ToDo"], summary="Move task to another stage")
async def move_task(task_id: int, stage_id: MoveTask):
    pass

@app.delete("/task/{task_id}", tags=["ToDo"], summary="Remove a task by id")
async def remove_task(task_id: int):
    pass


class TaskDescriptionUpdate(BaseModel):
    description: str

@app.patch("/task/{task_id}/description", tags=["ToDo"], summary="Update the description of the task")
async def update_description(task_id: int, update_data: TaskDescriptionUpdate):
    pass


class TaskExecutor(BaseModel):
    task_id: int

@app.patch("/task/executor/{user_id}", tags=["ToDo"], summary="Accept task")
async def assign_to(user_id: int, assign_data: TaskExecutor):
    pass

@app.patch("/task/{task_id}/status", tags=["ToDo"], summary="Change the status of the task")
async def change_status(task_id: int):
    pass

@app.get("/task/{task_id}/comments", tags=["ToDo"], summary="Get the comments on the task")
async def get_comments(task_id: int):
    pass


class CommentToRemove(BaseModel):
    comment_id: int

@app.delete("/task/{task_id}/comments", tags=["ToDo"], summary="Remove the comments on task")
async def remove_comment(task_id: int, remove_data: CommentToRemove):
    pass



async def main():
    await AsyncORM.initial_startup()
    await AsyncORM.insert_simple_data()

if __name__ == "__main__":
    asyncio.run(main())