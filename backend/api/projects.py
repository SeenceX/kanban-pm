from fastapi import APIRouter, HTTPException
from backend.models.queries.orm import AsyncORM
from backend.schemes.projects import Project, NewProject


router = APIRouter(
    prefix="/projects",
    tags=["Project"]
)


@router.get("/all", summary="Get all projects")
async def get_projects() -> list[Project]:
    return await AsyncORM.select_projects()

@router.get("/project/{creator_id}", summary="Get project by creator id")
async def get_projects_by_creator_id(creator_id: int) -> list[Project]:
    projects = await AsyncORM.select_projects()
    result = []
    for project in projects:
        if project.creator_id == creator_id:
            result.append(project)
    
    if len(result) > 0:
        return result
    else:
        raise HTTPException(status_code=404, detail="Projects not found")

@router.post("/project", summary="Post project")
async def create_project(new_project: NewProject) -> int:
    project = {
        "title": new_project.title,
        "creator_id": new_project.creator_id
    }

    return await AsyncORM.create_project(project)


@router.get("/project_membership/{id}", summary="Get project where subject is a member by his id")
async def get_project_memberships(id: int):
    result = await AsyncORM.get_project_memberships(id)
    return result
