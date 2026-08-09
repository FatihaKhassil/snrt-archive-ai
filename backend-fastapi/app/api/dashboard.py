from fastapi import APIRouter, Depends

from app.security.roles import RoleChecker
from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

service = DashboardService()


@router.get("/stats")
async def get_dashboard_statistics(
    current_user=Depends(RoleChecker(["ADMIN"]))
):

    return await service.get_statistics()