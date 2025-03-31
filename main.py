from fastapi import FastAPI, HTTPException, status
#from routes import users
import uvicorn
from schemas.queries.orm import AsyncORM
from pydantic import BaseModel, EmailStr, Field
import asyncio

app = FastAPI()

#app.include_router(users.router)
# uvicorn app:app

@app.get("/")
def read_root():
    return {"Hello": "World"}


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


@app.get("/projects", tags=["Projects"], summary="Get all projects")
async def get_projects():
    return await AsyncORM.select_projects()

@app.get("/project/{creator_id}", tags=["Projects"], summary="Get project by creator id")
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

@app.post("/projects", tags=["Projects"], summary="Post project")
async def create_project(new_project: NewProject):
    project = {
        "title": new_project.title,
        "creator_id": new_project.creator_id
    }

    await AsyncORM.create_project(project)


class NewMember(BaseModel):
    user_email: EmailStr
    project_id: int

@app.post("/projects/add_member", tags=["Projects"], summary="Add member to project")
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



# async def main():
#     await AsyncORM.initial_startup()
#     await AsyncORM.insert_simple_data()

# if __name__ == "__main__":
#     asyncio.run(main())