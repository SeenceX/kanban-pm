from fastapi import FastAPI, HTTPException, status
#from routes import users
import uvicorn
from schemas.queries.orm import AsyncORM
from pydantic import BaseModel, EmailStr, Field

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
    

if __name__ == "__app__":
    uvicorn.run("app.py", reload=True)