from pydantic import BaseModel, Field, EmailStr


class Stage(BaseModel):
    id: int
    name: str
    limit: int | None
    position: int
    project_id: int


class NewStage(BaseModel):
    name: str
    project_id: int


class RemoveStage(BaseModel):
    stage_id: int
    project_id: int


class MoveStage(BaseModel):
    new_position: int = Field(..., gt=0, description="Новая позиция (начиная с 1)")


class NewLimit(BaseModel):
    limit: int = Field(gt=0, description="Количество незавершенных задач этапа")