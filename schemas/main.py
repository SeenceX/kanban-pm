from sqlalchemy import select, func
from sqlalchemy.orm import Session
from database import async_engine
import asyncio

from queries.orm import AsyncORM

session = Session(async_engine)

async def main():
    await AsyncORM.initial_startup
    await AsyncORM.insert_simple_data


if __name__ == "__main__":
    asyncio.run(main())