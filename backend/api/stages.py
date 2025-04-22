from fastapi import APIRouter, HTTPException
from backend.models.queries.orm import AsyncORM
from backend.schemes.stages import Stage, NewStage, RemoveStage, MoveStage, NewLimit


router = APIRouter(
    prefix="/project/stages",
    tags=["Project stages"]
)


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
async def get_stages(project_id: int) -> list[Stage]:
    return await AsyncORM.get_stages(project_id)

@router.patch("{stage_id}/limit", summary="set the limit on the stage")
async def set_limit(stage_id: int, new_limit: NewLimit):
    data = {
        "stage_id": stage_id,
        "limit": new_limit.limit
    }
    
    result = await AsyncORM.set_limit(data)

    if not result:
        raise HTTPException(status_code=404, detail="Stage not found")
    
    return {"status": "success", "message": "The stage limit has been updated"}