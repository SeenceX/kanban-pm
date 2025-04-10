from pydantic import BaseModel, Field, EmailStr

class Project(BaseModel):
    id: int
    title: str
    creator_id: int


class NewProject(BaseModel):
    title: str = Field(max_length=50)
    creator_id: int