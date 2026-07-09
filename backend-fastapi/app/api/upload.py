from fastapi import APIRouter, UploadFile, File

from app.schemas.response_schema import ApiResponse
from app.services.upload_service import UploadService

router = APIRouter(
    prefix="/api/v1/upload",
    tags=["Upload"]
)

service = UploadService()


@router.post("/", response_model=ApiResponse)
async def upload_file(
    file: UploadFile = File(...)
):

    print("========== Upload endpoint called ==========")

    document_id = await service.upload(file)

    return ApiResponse(
        success=True,
        message="Document uploaded successfully.",
        data={
            "document_id": document_id
        }
    )