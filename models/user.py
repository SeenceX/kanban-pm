from typing import List, Optional
from pydantic import BaseModel

class Project(BaseModel):
    name: str


class Task(BaseModel):
    title: str


Role = str

class User(BaseModel):
    id: int
    name: str
    email: str
    projects: Optional[List[Project]] = None
    tasks: Optional[List[Task]] = None
    role: Role