import httpx


class EmbeddingService:

    def __init__(self):

        self.url = "http://ollama:11434/api/embeddings"

        self.model = "nomic-embed-text"


    async def generate_embedding(

        self,

        text: str

    ):

        async with httpx.AsyncClient() as client:

            response = await client.post(

                self.url,

                json={

                    "model": self.model,

                    "prompt": text

                }

            )

        response.raise_for_status()

        return response.json()["embedding"]