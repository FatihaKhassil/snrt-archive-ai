from app.database.mongodb import database


class DocumentRepository:

    def __init__(self):
        self.collection = database["documents"]

    async def create(self, document: dict):

        result = await self.collection.insert_one(document)

        return str(result.inserted_id)

    async def get_by_sha256(self, sha256: str):

        return await self.collection.find_one(
            {"sha256": sha256}
        )