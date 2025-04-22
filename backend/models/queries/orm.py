from sqlalchemy import Integer, and_, cast, func, insert, inspect, not_, or_, select, text, delete, update
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from passlib.context import CryptContext

from backend.models.database import Base, async_engine, session_factory
from backend.models.models import User, Project, ProjectMembership, Stage, Task, Comment, Role


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AsyncORM:

    @staticmethod
    async def initial_startup():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_sample_data():
        async with session_factory() as session:
            user_andrew = User(username="andrew", email="andrew@mail.ru", password=pwd_context.hash("hash1"))
            user_maria = User(username="maria", email="maria@gmail.com", password=pwd_context.hash("hash2"))
            session.add_all([user_andrew, user_maria])
            await session.flush()

            project1 = Project(title="My great project", creator_id=1)
            project2 = Project(title="My great project2", creator_id=1)
            session.add_all([project1, project2])
            await session.flush()

            stage1 = Stage(name="ToDo", position=1, limit=None, project_id=1)
            stage2 = Stage(name="In Progress", position=2, limit=5, project_id=1)
            stage3 = Stage(name="Done", position=3, limit=3, project_id=1)
            stage4 = Stage(name="ToDo", position=3, limit=3, project_id=2)
            session.add_all([stage1, stage2, stage3, stage4])
            await session.flush()

            task1 = Task(title="task1", description="Почистить кэш", status=False, stage_id=1, creator_id=2, assigned_user_id=None)
            task2 = Task(title="task2", description="Разработать запрос на удаление", status=False, stage_id=2, creator_id=1, assigned_user_id=1)
            task3 = Task(title="task3", description="Разработать интерфейс", status=False, stage_id=2, creator_id=1, assigned_user_id=2)
            task4 = Task(title="task4", description="Разработать API", status=True, stage_id=3, creator_id=1, assigned_user_id=None)
            task5 = Task(title="task5", description="Протестировать API", status=False, stage_id=1, creator_id=1, assigned_user_id=None)
            task6 = Task(title="task6", description="Улыбнуться", status=False, stage_id=1, creator_id=2, assigned_user_id=2)
            
            session.add_all([task1, task2, task3, task4, task5, task6])
            await session.flush()

            comment1 = Comment(text="Привет!", task_id=2, author_id=1)
            comment2 = Comment(text="Привет!", task_id=2, author_id=2)
            comment3 = Comment(text="Получается?", task_id=2, author_id=1)
            comment4 = Comment(text="Да", task_id=2, author_id=2)
            comment5 = Comment(text="Нужно обдумать", task_id=5, author_id=1)

            session.add_all([comment1, comment2, comment3, comment4, comment5])
            await session.flush()

            role1 = Role(name="creator", permissions=["all"])
            role2 = Role(name="member", permissions=["view", "comment", "execute", "move"])
            role3 = Role(name="guest", permissions=["view"])
            session.add_all([role1, role2, role3])

            project_membership1 = ProjectMembership(1, )

            await session.commit()

    @staticmethod
    async def authenticate_user(email: str, password: str):
        async with session_factory() as session:
            result = await session.execute(
                select(User)
                .where(User.email == email)
                )
            user = result.scalar_one_or_none()
            print(user)
            if not user or not pwd_context.verify(password, user.password):
                return None
            return user

    @staticmethod
    async def insert_user(user_data: dict) -> int:
        async with session_factory() as session:
            
            hashed_password = pwd_context.hash(user_data["password"])

            new_user = User(
                username=user_data["username"],
                email=user_data["email"],
                password=hashed_password
                )

            session.add(new_user)
            await session.flush()

            user_id = new_user.id
            print(f"Generated ID: ", user_id)

            await session.commit()

            return user_id


    @staticmethod
    async def select_users():
        async with session_factory() as session:
            query = select(User)
            result = await session.execute(query)
            users = result.scalars().all()
            return users
        

    @staticmethod
    async def select_projects():
        async with session_factory() as session:
            query = select(Project)
            result = await session.execute(query)
            projects = result.scalars().all()
            return projects
        

    @staticmethod
    async def get_project_memberships(id: int):
        async with session_factory() as session:
            query = (
                select(Project)
                .join(ProjectMembership, Project.id == ProjectMembership.project_id)
                .where(
                    ProjectMembership.user_id == id,
                    ProjectMembership.role_id == 2
                )
            )

            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def create_project(project_data: dict):
        async with session_factory() as session:
            new_project = Project(
                title=project_data["title"],
                creator_id=project_data["creator_id"]
            )

            session.add(new_project)
            
            await session.flush()

            project_id = new_project.id

            new_project_membership = ProjectMembership(
                user_id=project_data["creator_id"],
                project_id=new_project.id,
                role_id=1
            )
            
            session.add(new_project_membership)

            await session.commit()

            return project_id

    @staticmethod
    async def add_member(data: dict):
        async with session_factory() as session:
            new_membership = ProjectMembership(
                user_id=data["user_id"],
                project_id=data["project_id"],
                role_id=2
            )
            session.add(new_membership)
            await session.flush()
            await session.commit()
            
    @staticmethod
    async def remove_member(data: dict):
        async with session_factory() as session:
            await session.execute(
                delete(ProjectMembership)
                .where(ProjectMembership.user_id == data["user_id"])
                .where(ProjectMembership.project_id == data["project_id"])
            )
            await session.commit()

    @staticmethod
    async def assign_role(data: dict):
        async with session_factory() as session:
            result = await session.execute(
                select(ProjectMembership)
                .where(ProjectMembership.project_id == data["project_id"])
                .where(ProjectMembership.user_id == data["user_id"])
            )
            membership = result.scalar_one_or_none()

            if not membership:
                return False
            
            membership.role_id = data["role_id"]
            await session.commit()
            return True

    @staticmethod
    async def create_stage(data: dict):
        async with session_factory() as session:
            result = await session.execute(
                select(func.max(Stage.position))
                .where(Stage.project_id == data["project_id"])
            )
            max_position = result.scalar() or 0

            stage = Stage(name=data["name"], position=max_position+1, limit=None, project_id=data["project_id"])
            
            session.add(stage)
            await session.flush()
            await session.commit()

    @staticmethod
    async def remove_stage(data: dict):
        async with session_factory() as session:
            await session.execute(
                delete(Stage)
                .where(Stage.id == data["stage_id"])
                .where(Stage.project_id == data["project_id"])
            )
            await session.commit()

    @staticmethod
    async def reorder_stages(project_id: int):
        async with session_factory() as session:
            result = await session.execute(
                select(Stage)
                .where(Stage.project_id == project_id)
                .order_by(Stage.position)
            )
            stages = result.scalars().all()

            for index, stage in enumerate(stages, start=1):
                stage.position = index
            
            await session.commit()

    @staticmethod
    async def move_stage(stage_id: int, data: dict):
        async with session_factory() as session:
            stage = await session.get(Stage, stage_id)
            if not stage:
                return False
            
            old_position = stage.position
            project_id = stage.project_id

            if old_position == data["new_position"]:
                return True
            
            if data["new_position"] > old_position:
                await session.execute(
                    update(Stage)
                    .where(Stage.project_id == project_id)
                    .where(Stage.position > old_position)
                    .where(Stage.position <= data["new_position"])
                    .values(position=Stage.position-1)
                )
            else:
                await session.execute(
                    update(Stage)
                    .where(Stage.project_id == project_id)
                    .where(Stage.position >= data["new_position"])
                    .where(Stage.position < old_position)
                    .values(position=Stage.position+1)
                )

            stage.position = data["new_position"]
            await session.commit()
            return True
        
    @staticmethod
    async def set_limit(data: dict):
        async with session_factory() as session:
            stage = await session.get(Stage, data["stage_id"])
            if not stage:
                return False
            
            await session.execute(
                update(Stage)
                .where(Stage.id == data["stage_id"])
                .values(limit=data["limit"]) 
            )

            await session.commit()
            return True
        
    @staticmethod
    async def get_stages(project_id: int):
        async with session_factory() as session:
            result = await session.execute(
                select(Stage)
                .where(Stage.project_id == project_id)
                .order_by(Stage.position)
            )
            projects = result.scalars().all()
            return projects

    @staticmethod
    async def get_tasks_by_project_id(project_id: int):
        async with session_factory() as session:
            result = await session.execute(
                select(
                    Task.id,
                    Task.title,
                    Task.status,
                    Task.stage_id,
                    Task.creator_id,
                    Task.assigned_user_id,
                    Stage.position
                )
                .join(Stage, Task.stage_id == Stage.id)
                .where(Stage.project_id == project_id)
                .order_by(Stage.position)
            )

            return [dict(row._asdict()) for row in result.all()]
    
    @staticmethod
    async def get_tasks_by_stage_id(stage_id: int):
        async with session_factory() as session:
            result = await session.execute(
                select(Task)
                .where(Task.stage_id == stage_id)
            )
            tasks = result.scalars().all()
            return tasks

    @staticmethod
    async def create_task(data: dict):
        async with session_factory() as session:
            # title, description, status, stage_id, creator_id, assigned_user_id
           # task1 = Task(title="task1", description="Почистить кэш", status=False, stage_id=1, creator_id=2, assigned_user_id=None)
            task = Task(
                title=data["title"],
                description=data["description"],
                status=data["status"],
                stage_id=data["stage_id"],
                creator_id=data["creator_id"],
                assigned_user_id=data["assigned_user_id"]
            )

            session.add(task)
            await session.flush()
            await session.commit()

    @staticmethod
    async def move_task(data: dict):
        async with session_factory() as session:
            await session.execute(
                    update(Task)
                    .where(Task.id == data["task_id"])
                    .values(stage_id=data["stage_id"])
                )
            
            await session.commit()

    @staticmethod
    async def delete_task(task_id: int):
        async with session_factory() as session:
            await session.execute(
                delete(Task)
                .where(Task.id == task_id)
            )
            await session.commit()
        
    @staticmethod
    async def update_description(task_id: int, new_description: str):
        async with session_factory() as session:
            await session.execute(
                update(Task)
                .where(Task.id == task_id)
                .values(description=new_description)
            )

            await session.commit()

    @staticmethod
    async def assing_to(task_id: int, user_id: int):
        async with session_factory() as session:
            await session.execute(
                update(Task)
                .where(Task.id == task_id)
                .values(assigned_user_id=user_id)
            )

            await session.commit()

    @staticmethod
    async def set_status(task_id: int):
        async with session_factory() as session:
            await session.execute(
                update(Task)
                .where(Task.id == task_id)
                .values(status=not_(Task.status))
            )

            await session.commit()

    @staticmethod
    async def get_comments(task_id: int):
        async with session_factory() as session:
            result = await session.execute(
                select(Comment)
                .where(Comment.task_id == task_id)
                .order_by(Comment.created_at)
            )
            return result.scalars().all()
            

    @staticmethod
    async def create_comment(data: dict):
        async with session_factory() as session:
            comment = Comment(
                text=data["text"],
                task_id=data["task_id"],
                author_id=data["author_id"]
            )

            session.add(comment)
            await session.flush()
            await session.commit()

    @staticmethod
    async def remove_comment(comment_id: int):
        async with session_factory() as session:
            await session.execute(
                delete(Comment)
                .where(Comment.id == comment_id)
            )
            await session.commit()