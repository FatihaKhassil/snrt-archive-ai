from bson import ObjectId

from mongodb import mongodb


class DocumentRepository:

    async def get_transcription(
        self,
        document_id
    ):

        document = await mongodb.documents.find_one(

            {
                "_id": ObjectId(
                    document_id
                )
            },

            {
                "transcription": 1
            }

        )

        if not document:

            return None

        return document.get(
            "transcription"
        )


    async def update_embedding_status(
        self,
        document_id
    ):

        await mongodb.documents.update_one(

            {
                "_id": ObjectId(
                    document_id
                )
            },

            {
                "$set": {

                    "status": "EMBEDDED",

                    "processing.embedding": True

                }

            }

        )