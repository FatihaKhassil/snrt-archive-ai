from fastapi import Depends, HTTPException

from app.security.dependencies import get_current_user


class RoleChecker:

    def __init__(self, allowed_roles: list[str]):

        self.allowed_roles = allowed_roles

    async def __call__(self, current_user=Depends(get_current_user)):

        role = current_user.get("role")

        if role not in self.allowed_roles:

            raise HTTPException(
                status_code=403,
                detail="You are not authorized to access this resource."
            )

        return current_user