from bson import ObjectId

from mongodb import documents_collection



class DocumentRepository:


    async def update_extracted_text(
        self,
        document_id,
        text
    ):


        await documents_collection.update_one(

            {
                "_id": ObjectId(document_id)
            },

            {
                "$set":
                {
                    "extracted_text": text,

                    "status": "TEXT_EXTRACTED",

                    "processing.transcription": True
                }
            }

        )