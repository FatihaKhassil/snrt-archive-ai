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

                    "summary": summary,

                    "keywords": keywords

                }

            }

        )