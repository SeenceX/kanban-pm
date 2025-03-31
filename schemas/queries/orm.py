from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from schemas.database import Base, async_engine, session_factory
from schemas.models import User, Project, ProjectMembership, Stage, Task, Comment


class AsyncORM:
    
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            #await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_user(user_data: dict):
        async with session_factory() as session:
            new_user = User(
                username=user_data["username"],
                email=user_data["email"],
                password=user_data["password"]
                )
            #user_andrew = User(username="andrew", email="andrew@mail.ru", password="hash1")
            #user_maria = User(username="maria", email="maria@gmail.com", password="hash2")
            #session.add_all([user_andrew, user_maria])
            session.add(new_user)
            await session.flush()
            await session.commit()


    @staticmethod
    async def select_users():
        async with session_factory() as session:
            query = select(User)
            result = await session.execute(query)
            users = result.scalars().all()
            #print(f"{users=}")
            return users

    @staticmethod
    async def select_projects():
        async with session_factory() as session:
            query = select(Project)
            result = await session.execute(query)
            projects = result.scalars().all()
            return projects

    @staticmethod
    async def create_project(project_data: dict):
        async with session_factory() as session:
            new_project = Project(
                title=project_data["title"],
                creator_id=project_data["creator_id"]
            )
            #project1 = Project(title="My great project", creator_id=1)
            #project2 = Project(title="My great project2", creator_id=1)
            #session.add_all([project1, project2])
            session.add(new_project)
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
            task1 = Task(title="task1", description="Почистить кэш", status=False, stage_id=1, creator_id=2, assigned_user_id=None)
            task2 = Task(title="task2", description="Разработать запрос на удаление", status=False, stage_id=2, creator_id=1, assigned_user_id=1)
            task3 = Task(title="task3", description="Разработать интерфейс", status=False, stage_id=2, creator_id=1, assigned_user_id=2)
            task4 = Task(title="task4", description="Разработать API", status=True, stage_id=3, creator_id=1, assigned_user_id=None)
            task5 = Task(title="task5", description="Протестировать API", status=False, stage_id=1, creator_id=1, assigned_user_id=None)
            task6 = Task(title="task6", description="Улыбнуться", status=False, stage_id=1, creator_id=2, assigned_user_id=2)
            
            session.add_all([task1, task2, task3, task4, task5, task6])
            await session.flush()
            await session.commit()

    @staticmethod
    async def create_comment():
        async with session_factory() as session:
            comment1 = Comment(text="Привет!", task_id=2, author_id=1)
            comment2 = Comment(text="Привет!", task_id=2, author_id=2)
            comment3 = Comment(text="Получается?", task_id=2, author_id=1)
            comment4 = Comment(text="Да", task_id=2, author_id=2)
            comment5 = Comment(text="Нужно обдумать", task_id=5, author_id=1)

            session.add_all([comment1, comment2, comment3, comment4, comment5])
            await session.flush()
            await session.commit()