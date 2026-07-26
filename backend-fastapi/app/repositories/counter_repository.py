from app.database.mongodb import database

from pymongo import ReturnDocument


class CounterRepository:

    def __init__(self):

        self.collection = database["counters"]


    async def get_next_sequence(

        self,

        counter_name: str

    ):

        counter = await self.collection.find_one_and_update(

            {

                "_id": counter_name

            },

            {

                "$inc": {

                    "sequence": 1

                }

            },

            upsert=True,

            return_document=ReturnDocument.AFTER

        )

        return counter["sequence"]