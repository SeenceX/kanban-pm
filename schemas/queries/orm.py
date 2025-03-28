from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload

from database import Base, async_engine, session_factory
from models import User, Project, ProjectMembership, Stage, Task


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
            project2 = Project(title="My great project2", creator_id=1)
            session.add_all([project1, project2])
            await session.flush()
            await session.commit()

    @staticmethod
    async def create_stage():
        async with session_factory() as session:
            stage1 = Stage(name="ToDo", position=1, limit=None, project_id=1)
            stage2 = Stage(name="In Progress", position=2, limit=5, project_id=1)
            stage3 = Stage(name="Done", position=3, limit=3, project_id=1)
            stage4 = Stage(name="ToDo", position=3, limit=3, project_id=2)
            session.add_all([stage1, stage2, stage3, stage4])
            await session.flush()
            await session.commit()

    @staticmethod
    async def create_task():
        async with session_factory() as session:
            # title, description, status, stage_id, creator_id, assigned_user_id
            task1 = Task(title="task1", description="Разработать API", status=False, stage_id=1, creator_id=2, assigned_user_id=1)
            task2 = Task(title="task2", description="Разработать API", status=False, stage_id=2, creator_id=1, assigned_user_id=1)
            task3 = Task(title="task3", description="Разработать API", status=False, stage_id=2, creator_id=1, assigned_user_id=2)
            task4 = Task(title="task4", description="Разработать API", status=True, stage_id=3, creator_id=1, assigned_user_id=None)
            task5 = Task(title="task5", description="Разработать API", status=False, stage_id=2, creator_id=1, assigned_user_id=2)
            task6 = Task(title="task6", description="Разработать API", status=False, stage_id=1, creator_id=2, assigned_user_id=2)
            session.add_all([task1, task2, task3, task4, task5, task6])
            await session.flush()
            await session.commit()