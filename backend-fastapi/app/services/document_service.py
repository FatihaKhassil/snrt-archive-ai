import os

from datetime import datetime

from fastapi import HTTPException

from app.repositories.document_repository import DocumentRepository
from app.services.chroma_service import ChromaService
from app.services.solr_service import SolrService


class DocumentService:

    def __init__(self):

        self.repository = DocumentRepository()

        self.chroma_service = ChromaService()

        self.solr_service = SolrService()


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

        # ============================================================
        # 1. Vérifier que le document existe
        # ============================================================

        document = await self.repository.get_by_id(

            document_id

        )

        if not document:

            return False


        # ============================================================
        # 2. Récupérer le chemin du fichier
        # ============================================================

        file_path = document.get(

            "storage_path"

        )


        # ============================================================
        # 3. Supprimer les embeddings de ChromaDB
        # ============================================================

        try:

            await self.chroma_service.delete_by_document_id(

                document_id

            )

            print(

                f"✅ ChromaDB nettoyé : {document_id}",

                flush=True

            )

        except Exception as e:

            print(

                f"❌ Erreur suppression ChromaDB : {e}",

                flush=True

            )

            raise HTTPException(

                status_code=500,

                detail="Erreur lors de la suppression des embeddings."

            )


        # ============================================================
        # 4. Supprimer l'index Solr
        # ============================================================

        try:

            await self.solr_service.delete_by_document_id(

                document_id

            )

            print(

                f"✅ Solr nettoyé : {document_id}",

                flush=True

            )

        except Exception as e:

            print(

                f"❌ Erreur suppression Solr : {e}",

                flush=True

            )

            raise HTTPException(

                status_code=500,

                detail="Erreur lors de la suppression de l'index Solr."

            )


        # ============================================================
        # 5. Supprimer le fichier physique
        # ============================================================

        if file_path:

            if os.path.exists(

                file_path

            ):

                try:

                    os.remove(

                        file_path

                    )

                    print(

                        f"✅ Fichier supprimé : {file_path}",

                        flush=True

                    )

                except Exception as e:

                    print(

                        f"❌ Erreur suppression fichier : {e}",

                        flush=True

                    )

                    raise HTTPException(

                        status_code=500,

                        detail="Erreur lors de la suppression du fichier."

                    )

            else:

                print(

                    f"⚠️ Fichier déjà absent : {file_path}",

                    flush=True

                )


        # ============================================================
        # 6. Supprimer le document MongoDB
        # ============================================================

        deleted = await self.repository.delete(

            document_id

        )

        if not deleted:

            raise HTTPException(

                status_code=500,

                detail="Le document n'a pas pu être supprimé de MongoDB."

            )


        print(

            f"✅ MongoDB nettoyé : {document_id}",

            flush=True

        )


        # ============================================================
        # 7. Suppression terminée
        # ============================================================

        print(

            f"🗑️ Document complètement supprimé : {document_id}",

            flush=True

        )

        return True


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

        if not file_path or not os.path.exists(

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