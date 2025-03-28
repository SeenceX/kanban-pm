from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload

from database import Base, async_engine, session_factory
from models import User, Project, ProjectMembership


class AsyncORM:
    
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_users():
        async with session_factory() as session:
            user_andrew = User(username="andrew", email="andrew@mail.ru", password="hash1")
            user_maria = User(username="maria", email="maria@gmail.com", password="hash2")
            session.add_all([user_andrew, user_maria])
            await session.flush()
            await session.commit()

    @staticmethod
    async def select_users():
        async with session_factory() as session:
            query = select(User)
            result = await session.execute(query)
            users = result.scalars().all()
            print(f"{users=}")

    @staticmethod
    async def create_project():
        async with session_factory() as session:
            project1 = Project(title="My great project", creator_id=1)
            session.add_all([project1])
            await session.flush()
            await session.commit()