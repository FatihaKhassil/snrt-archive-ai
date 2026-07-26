from app.repositories.counter_repository import CounterRepository


class CounterService:

    def __init__(self):

        self.repository = CounterRepository()


    async def next_user_id(

        self

    ):

        sequence = await self.repository.get_next_sequence(

            "users"

        )

        return f"USR-{sequence:06d}"


    async def next_document_id(

        self

    ):

        sequence = await self.repository.get_next_sequence(

            "documents"

        )

        return f"DOC-{sequence:06d}"