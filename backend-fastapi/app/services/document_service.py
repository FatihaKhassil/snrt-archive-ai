import os

from datetime import datetime

from fastapi import HTTPException

from app.repositories.document_repository import DocumentRepository


class DocumentService:

    def __init__(self):

        self.repository = DocumentRepository()


    async def get_all_documents(

        self

    ):

        return await self.repository.get_all()


    async def get_document_by_id(

        self,

        document_id: str

    ):

        return await self.repository.get_by_id(

            document_id

        )


    async def update_document(

        self,

        document_id: str,

        request

    ):

        document = await self.repository.get_by_id(

            document_id

        )

        if not document:

            return False

        data = {

            "title": request.title,

            "ai_metadata.summary": request.summary,

            "ai_metadata.keywords": request.keywords,

            "updated_at": datetime.utcnow().isoformat()

        }

        return await self.repository.update(

            document_id,

            data

        )


    async def delete_document(

        self,

        document_id: str

    ):

        document = await self.repository.get_by_id(

            document_id

        )

        if not document:

            return False

        file_path = document.get(

            "storage_path"

        )

        if file_path and os.path.exists(

            file_path

        ):

            os.remove(

                file_path

            )

        return await self.repository.delete(

            document_id

        )


    async def download_document(

        self,

        document_id: str

    ):

        document = await self.repository.get_by_id(

            document_id

        )

        if not document:

            raise HTTPException(

                status_code=404,

                detail="Document not found"

            )

        file_path = document.get(

            "storage_path"

        )

        if not os.path.exists(

            file_path

        ):

            raise HTTPException(

                status_code=404,

                detail="File not found"

            )

        return {

            "path": file_path,

            "filename": document["original_filename"]

        }