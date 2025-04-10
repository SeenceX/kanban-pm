from fastapi import FastAPI, HTTPException, status
from api import comments, users, projects, stages, members, tasks
import uvicorn
from models.queries.orm import AsyncORM
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
            "name": "Tasks",
            "description": "Операции с задачами"
        },
        {
            "name": "Comments",
            "description": "Операции с комментариями"
        }
    ]
)

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(stages.router)
app.include_router(members.router)
app.include_router(tasks.router)
app.include_router(comments.router)

async def main():
    await AsyncORM.initial_startup()
    await AsyncORM.insert_simple_data()

if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)