from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.schemas.document_update_request import DocumentUpdateRequest
from app.services.document_service import DocumentService


router = APIRouter(

    prefix="/documents",

    tags=["Documents"]

)

service = DocumentService()


@router.get("")

async def get_documents():

    return await service.get_all_documents()


@router.get("/{document_id}")

async def get_document(

    document_id: str

):

    document = await service.get_document_by_id(

        document_id

    )

    if not document:

        raise HTTPException(

            status_code=404,

            detail="Document not found"

        )

    return document


@router.get("/{document_id}/download")

async def download_document(

    document_id: str

):

    file = await service.download_document(

        document_id

    )

    return FileResponse(

        path=file["path"],

        filename=file["filename"],

        media_type="application/octet-stream"

    )


@router.put("/{document_id}")

async def update_document(

    document_id: str,

    request: DocumentUpdateRequest

):

    updated = await service.update_document(

        document_id,

        request

    )

    if not updated:

        raise HTTPException(

            status_code=404,

            detail="Document not found"

        )

    return {

        "message": "Document updated successfully."

    }


@router.delete("/{document_id}")

async def delete_document(

    document_id: str

):

    deleted = await service.delete_document(

        document_id

    )

    if not deleted:

        raise HTTPException(

            status_code=404,

            detail="Document not found"

        )

    return {

        "message": "Document deleted successfully."

    }