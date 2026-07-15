from bson import ObjectId

from app.database.mongodb import database


class DocumentRepository:

    def __init__(self):

        self.collection = database["documents"]


    async def create(

        self,

        document: dict

    ):

        result = await self.collection.insert_one(

            document

        )

        return str(

            result.inserted_id

        )


    async def get_by_sha256(

        self,

        sha256: str

    ):

        return await self.collection.find_one(

            {

                "sha256": sha256

            }

        )


    async def get_by_id(

        self,

        document_id: str

    ):

        document = await self.collection.find_one(

            {

                "_id": ObjectId(

                    document_id

                )

            }

        )

        if document:

            document["_id"] = str(

                document["_id"]

            )

        return document


    async def get_documents(

        self,

        ids: list[str]

    ):

        object_ids = [

            ObjectId(

                document_id

            )

            for document_id in ids

        ]

        cursor = self.collection.find(

            {

                "_id": {

                    "$in": object_ids

                }

            }

        )

        documents = await cursor.to_list(

            length=None

        )

        for document in documents:

            document["_id"] = str(

                document["_id"]

            )

        return documents