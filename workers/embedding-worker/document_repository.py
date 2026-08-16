from bson import ObjectId

from mongodb import mongodb


class DocumentRepository:

    async def get_text(
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
                "transcription": 1,
                "extracted_text": 1
            }

        )

        if not document:

            return None

        # Audio traité par Whisper
        if document.get("transcription"):

            return document.get(
                "transcription"
            )

        # PDF / DOCX traité par Tika
        if document.get("extracted_text"):

            return document.get(
                "extracted_text"
            )

        return None


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