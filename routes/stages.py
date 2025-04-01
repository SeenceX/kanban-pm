from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, EmailStr
from schemas.queries.orm import AsyncORM

router = APIRouter(
    prefix="/project/stages",
    tags=["Project stages"]
)

class NewStage(BaseModel):
    name: str
    project_id: int


class RemoveStage(BaseModel):
    stage_id: int
    project_id: int


class MoveStage(BaseModel):
    new_position: int = Field(..., gt=0, description="Новая позиция (начиная с 1)")



@router.post("/create_stage", summary="Add stage to project")
async def create_stage(stage_data: NewStage):
    data = {
        "name": stage_data.name,
        "project_id": stage_data.project_id
    }
    return await AsyncORM.create_stage(data)

@router.delete("/remove_stage", summary="Remove a stage from project")
async def create_stage(remove_stage_data: RemoveStage):
    data = {
        "stage_id": remove_stage_data.stage_id,
        "project_id": remove_stage_data.project_id
    }
    await AsyncORM.remove_stage(data)
    await AsyncORM.reorder_stages(data["project_id"])

@router.get("/reorder_project_stages", summary="Пересчет порядка этапов", deprecated=True)
async def reorder_stages(project_id: int):
    await AsyncORM.reorder_stages(project_id)

@router.patch("/{stage_id}/move_stage", summary="Move a stage")
async def move_stage(stage_id: int, move_stage_data: MoveStage):

    data = {
        "new_position": move_stage_data.new_position
    }

    result = await AsyncORM.move_stage(stage_id, data)

    if not result:
        raise HTTPException(status_code=404, detail="Stage not found or invalid position")
    
    return {"status": "success", "message": "Stage position updated"}

@router.get("/{project_id}", summary="Get all stages of a project")
async def get_stages(project_id: int):
    return await AsyncORM.get_stages(project_id)

@router.patch("/limit", tags=["ToDo"], summary="set the limit on the stage")
async def set_limit():
    pass