from datetime import datetime

from fastapi import HTTPException

from app.repositories.user_repository import UserRepository
from app.services.counter_service import CounterService
from app.security.password import hash_password


class UserService:

    def __init__(self):

        self.repository = UserRepository()

        self.counter_service = CounterService()


    async def create_user(

        self,

        request

    ):

        existing_user = await self.repository.get_by_email(

            request.email

        )

        if existing_user:

            raise HTTPException(

                status_code=409,

                detail="Email already exists."

            )

        user = {

            "user_id": await self.counter_service.next_user_id(),

            "first_name": request.first_name,

            "last_name": request.last_name,

            "email": request.email,

            "phone": request.phone,

            "department": request.department,

            "role": request.role,

            "status": "ACTIVE",

            "password": hash_password("123456"),

            "created_at": datetime.utcnow().isoformat(),

            "updated_at": datetime.utcnow().isoformat()

        }

        await self.repository.create(

            user

        )

        return {

            "message": "User created successfully."

        }


    async def get_all_users(

        self

    ):

        return await self.repository.get_all()


    async def get_user_by_id(

        self,

        user_id: str

    ):

        user = await self.repository.get_by_user_id(

            user_id

        )

        if not user:

            raise HTTPException(

                status_code=404,

                detail="User not found."

            )

        return user


    async def update_user(

        self,

        user_id: str,

        request

    ):

        user = await self.repository.get_by_user_id(

            user_id

        )

        if not user:

            raise HTTPException(

                status_code=404,

                detail="User not found."

            )

        existing_user = await self.repository.get_by_email(

            request.email

        )

        if existing_user and existing_user["user_id"] != user_id:

            raise HTTPException(

                status_code=409,

                detail="Email already exists."

            )

        data = {

            "first_name": request.first_name,

            "last_name": request.last_name,

            "email": request.email,

            "phone": request.phone,

            "department": request.department,

            "role": request.role,

            "status": request.status,

            "updated_at": datetime.utcnow().isoformat()

        }

        await self.repository.update(

            user_id,

            data

        )

        return {

            "message": "User updated successfully."

        }


    async def delete_user(

        self,

        user_id: str

    ):

        user = await self.repository.get_by_user_id(

            user_id

        )

        if not user:

            raise HTTPException(

                status_code=404,

                detail="User not found."

            )

        await self.repository.delete(

            user_id

        )

        return {

            "message": "User deleted successfully."

        }