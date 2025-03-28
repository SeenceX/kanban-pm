from sqlalchemy import select, func
from sqlalchemy.orm import Session
from models import User
from database import async_engine
import asyncio

from queries.orm import AsyncORM

session = Session(async_engine)

async def main():
    await AsyncORM.create_tables()
    await AsyncORM.insert_users()
    await AsyncORM.select_users()


if __name__ == "__main__":
    asyncio.run(main())