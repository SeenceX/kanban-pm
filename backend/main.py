from fastapi import FastAPI, HTTPException, status
from backend.api import comments, users, projects, stages, members, tasks
import uvicorn
from backend.models.queries.orm import AsyncORM
from pydantic import BaseModel, EmailStr, Field
from fastapi.middleware.cors import CORSMiddleware

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

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://127.0.0.1:3000",
    "http://0.0.0.0:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(stages.router)
app.include_router(members.router)
app.include_router(tasks.router)
app.include_router(comments.router)

async def main():
    await AsyncORM.initial_startup()
    await AsyncORM.insert_sample_data()

if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)