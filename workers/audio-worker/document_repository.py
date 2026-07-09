from bson import ObjectId

from mongodb import documents_collection


class DocumentRepository:

    async def update_transcription(
        self,
        document_id,
        transcription
    ):

        await documents_collection.update_one(
            {
                "_id": ObjectId(document_id)
            },
            {
                "$set": {
                    "transcription": transcription,
                    "status": "TRANSCRIBED"
                }
            }
        )