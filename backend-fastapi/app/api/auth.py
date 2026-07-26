from fastapi import APIRouter

from app.schemas.login_request import LoginRequest
from app.services.auth_service import AuthService


router = APIRouter(

    prefix="/auth",

    tags=["Authentication"]

)

service = AuthService()


@router.post("/login")

async def login(

    request: LoginRequest

):

    return await service.login(

        request

    )