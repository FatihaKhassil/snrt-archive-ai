from app.database.mongodb import database


class UserRepository:

    def __init__(self):

        self.collection = database["users"]


    async def create(

        self,

        user: dict

    ):

        await self.collection.insert_one(

            user

        )


    async def get_all(

        self

    ):

        cursor = self.collection.find().sort(

            "created_at",

            -1

        )

        users = await cursor.to_list(

            length=None

        )

        for user in users:

            user.pop(

                "_id",

                None

            )

        return users


    async def get_by_user_id(

        self,

        user_id: str

    ):

        user = await self.collection.find_one(

            {

                "user_id": user_id

            }

        )

        if user:

            user.pop(

                "_id",

                None

            )

        return user


    async def get_by_email(

        self,

        email: str

    ):

        user = await self.collection.find_one(

            {

                "email": email

            }

        )

        if user:

            user.pop(

                "_id",

                None

            )

        return user


    async def update(

        self,

        user_id: str,

        data: dict

    ):

        result = await self.collection.update_one(

            {

                "user_id": user_id

            },

            {

                "$set": data

            }

        )

        return result.modified_count > 0


    async def delete(

        self,

        user_id: str

    ):

        result = await self.collection.delete_one(

            {

                "user_id": user_id

            }

        )

        return result.deleted_count > 0