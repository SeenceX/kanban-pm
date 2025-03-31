from sqlalchemy import select, func
from sqlalchemy.orm import Session
from database import async_engine
import asyncio

from queries.orm import AsyncORM

session = Session(async_engine)

async def main():
    #await AsyncORM.create_tables()
    #await AsyncORM.insert_users()
    await AsyncORM.select_users()
    #await AsyncORM.create_project()
    #await AsyncORM.create_stage()
    #await AsyncORM.create_task()
    #await AsyncORM.create_comment()


if __name__ == "__main__":
    asyncio.run(main())