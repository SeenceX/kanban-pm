from fastapi import FastAPI, HTTPException, status
from routes import users, projects, stages, members, tasks
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

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(stages.router)
app.include_router(members.router)
app.include_router(tasks.router)

async def main():
    await AsyncORM.initial_startup()
    await AsyncORM.insert_simple_data()

if __name__ == "__main__":
    asyncio.run(main())