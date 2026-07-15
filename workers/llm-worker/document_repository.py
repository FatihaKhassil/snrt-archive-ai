from bson import ObjectId

from mongodb import mongodb


class DocumentRepository:

    async def update_llm_result(
        self,
        document_id,
        summary,
        keywords
    ):

        await mongodb.documents.update_one(

            {
                "_id": ObjectId(
                    document_id
                )
            },

            {
                "$set": {

                    "status": "LLM_PROCESSED",

                    "ai_metadata.summary": summary,
                    "ai_metadata.keywords": keywords,

                    "processing.summary": True

                }

            }

        )