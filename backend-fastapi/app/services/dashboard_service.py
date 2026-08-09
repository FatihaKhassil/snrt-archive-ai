from app.repositories.user_repository import UserRepository
from app.repositories.document_repository import DocumentRepository


class DashboardService:

    def __init__(self):

        self.user_repository = UserRepository()
        self.document_repository = DocumentRepository()

    async def get_statistics(self):

        users = await self.user_repository.get_all()
        documents = await self.document_repository.get_all()

        # ==========================
        # USERS
        # ==========================

        total_users = len(users)

        admins = len([
            user
            for user in users
            if user.get("role") == "ADMIN"
        ])

        documentalists = len([
            user
            for user in users
            if user.get("role") == "DOCUMENTALIST"
        ])

        standard_users = len([
            user
            for user in users
            if user.get("role") == "USER"
        ])

        active_users = len([
            user
            for user in users
            if user.get("status") == "ACTIVE"
        ])

        # ==========================
        # DOCUMENTS
        # ==========================

        total_documents = len(documents)

        audio_documents = len([
            document
            for document in documents
            if document.get("file_type") == "audio"
        ])

        other_documents = len([
            document
            for document in documents
            if document.get("file_type") == "document"
        ])

        # ==========================
        # PROCESSING
        # ==========================

        transcribed = len([
            document
            for document in documents
            if document.get("transcription")
        ])

        summarized = len([
            document
            for document in documents
            if document.get("ai_metadata", {}).get("summary")
        ])

        keyworded = len([
            document
            for document in documents
            if len(
                document.get("ai_metadata", {}).get("keywords", [])
            ) > 0
        ])

        indexed = len([
            document
            for document in documents
            if document.get("status") == "INDEXED"
        ])

        uploaded = len([
            document
            for document in documents
            if document.get("status") == "UPLOADED"
        ])

        processing = len([
            document
            for document in documents
            if document.get("status") == "PROCESSING"
        ])

        completed = len([
            document
            for document in documents
            if document.get("status") == "COMPLETED"
        ])

        failed = len([
            document
            for document in documents
            if document.get("status") == "FAILED"
        ])

        return {

            "users": {

                "total": total_users,
                "admins": admins,
                "documentalists": documentalists,
                "standard_users": standard_users,
                "active": active_users

            },

            "documents": {

                "total": total_documents,
                "audio": audio_documents,
                "documents": other_documents

            },

            "processing": {

                "transcribed": transcribed,
                "summarized": summarized,
                "keywords": keyworded,
                "indexed": indexed

            },

            "status": {

                "uploaded": uploaded,
                "processing": processing,
                "completed": completed,
                "failed": failed

            }

        }