from fastapi import APIRouter, HTTPException
from models.queries.orm import AsyncORM
from schemes.members import NewMember, AssignRole, RemoveMember


router = APIRouter(
    prefix="/project/members",
    tags=["Project members"]
)


@router.post("/add", summary="Add member to project")
async def add_member(new_member: NewMember):
    data = {
        "email": new_member.user_email,
        "project_id": new_member.project_id,
    }

    is_finded = False
    users = await AsyncORM.select_users()
    for user in users:
        if user.email == data["email"]:
            data["user_id"] = user.id
            is_finded = True
    
    if not is_finded:
        raise HTTPException(status_code=404, detail="User not found")
    
    await AsyncORM.add_member(data)
    
    print(data)

@router.delete("/remove", summary="Remove a member from project")
async def remove_member(remove_member_data: RemoveMember):
    data = {
        "project_id": remove_member_data.project_id,
        "user_id": remove_member_data.user_id
    }
    return await AsyncORM.remove_member(data)
    
@router.put("/assign_role", summary="Assign role to member")
async def assign_role(assign_member_role_date: AssignRole):
    data = {
        "project_id": assign_member_role_date.project_id,
        "user_id": assign_member_role_date.user_id,
        "role_id": assign_member_role_date.role_id
    }
    
    result = await AsyncORM.assign_role(data)

    if not result:
        raise HTTPException(status_code=404, detail="Membership not found")
    
    return {"status": "success", "message": "Role updated"}