from .main import app
import uvicorn
import asyncio
from backend.models.queries.orm import AsyncORM

async def main():
    await AsyncORM.initial_startup()
    await AsyncORM.insert_sample_data()


if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)