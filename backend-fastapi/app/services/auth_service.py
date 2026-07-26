from fastapi import HTTPException

from app.repositories.user_repository import UserRepository
from app.security.password import verify_password
from app.security.jwt import create_access_token


class AuthService:

    def __init__(self):

        self.repository = UserRepository()


    async def login(

        self,

        request

    ):

        user = await self.repository.get_by_email(

            request.email

        )

        if not user:

            raise HTTPException(

                status_code=401,

                detail="Invalid email or password."

            )

        if not verify_password(

            request.password,

            user["password"]

        ):

            raise HTTPException(

                status_code=401,

                detail="Invalid email or password."

            )

        token = create_access_token(

            {

                "user_id": user["user_id"],

                "role": user["role"]

            }

        )

        return {

            "access_token": token,

            "token_type": "bearer",

            "user_id": user["user_id"],

            "role": user["role"],

            "first_name": user["first_name"]

        }