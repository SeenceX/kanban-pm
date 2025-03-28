import datetime
import enum
from typing import Annotated, List

from sqlalchemy import (
    JSON,
    TIMESTAMP,
    CheckConstraint,
    Column,
    Enum,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    String,
    Table,
    text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.now(datetime.timezone.utc)
)]


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(String(20), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str]

    created_projects: Mapped[List["Project"]] = relationship(
        back_populates="creator",
        cascade="all, delete-orphan"
    )

    created_tasks: Mapped[List["Task"]] = relationship(
        back_populates="creator",
        foreign_keys="[Task.creator_id]"
    )

    assigned_tasks: Mapped[List["Task"]] = relationship(
        back_populates="assigned_user",
        foreign_keys="[Task.assigned_user_id]"
    )

    project_memberships: Mapped[List["ProjectMembership"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(50))
    
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    creator: Mapped["User"] = relationship(back_populates="created_projects")

    user_memberships: Mapped[List["ProjectMembership"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan"
    )

    stages: Mapped[List["Stage"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        order_by="Stage.position"
    )


class ProjectMembership(Base):
    __tablename__ = "project_memberships"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)

    user: Mapped["User"] = relationship(back_populates="project_memberships")
    project: Mapped["Project"] = relationship(back_populates="user_memberships")



class Stage(Base):
    __tablename__ = "stages"
    
    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(50))
    position: Mapped[int]
    limit: Mapped[int | None]

    tasks: Mapped[List["Task"]] = relationship(
        back_populates="stage",
        cascade="all, delete-orphan",
        order_by="Task.id"
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        index=True
    )
    project: Mapped["Project"] = relationship(back_populates="stages")


class Task(Base):
    __tablename__ = "tasks"
    
    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str]
    status: Mapped[bool]

    stage_id: Mapped[int] = mapped_column(
        ForeignKey("stages.id", ondelete="CASCADE"),
        index=True
    )
    stage: Mapped["Stage"] = relationship(back_populates="tasks")

    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    creator: Mapped["User"] = relationship(back_populates="created_tasks", foreign_keys=[creator_id])
    
    assigned_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    assigned_user: Mapped["User"] = relationship(back_populates="assigned_tasks", foreign_keys=[assigned_user_id])
    

