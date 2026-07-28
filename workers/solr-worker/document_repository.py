from bson import ObjectId

from mongodb import database


class DocumentRepository:

    def __init__(self):

        self.collection = database.documents

    async def get_document(
        self,
        document_id: str
    ):

        return await self.collection.find_one(
            {
                "_id": ObjectId(document_id)
            }
        )

    async def update_solr_status(
        self,
        document_id: str
    ):

        await self.collection.update_one(

            {
                "_id": ObjectId(document_id)
            },

            {
                "$set": {

                    "status": "INDEXED",

                    "processing.indexation": True

                }

            }

        )