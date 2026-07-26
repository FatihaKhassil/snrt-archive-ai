from fastapi import APIRouter

from app.schemas.user_create_request import UserCreateRequest
from app.schemas.user_update_request import UserUpdateRequest
from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

service = UserService()


@router.post("")
async def create_user(
    request: UserCreateRequest
):
    return await service.create_user(
        request
    )


@router.get("")
async def get_users():
    return await service.get_all_users()


@router.get("/{user_id}")
async def get_user(
    user_id: str
):
    return await service.get_user_by_id(
        user_id
    )


@router.put("/{user_id}")
async def update_user(
    user_id: str,
    request: UserUpdateRequest
):
    return await service.update_user(
        user_id,
        request
    )


@router.delete("/{user_id}")
async def delete_user(
    user_id: str
):
    return await service.delete_user(
        user_id
    )