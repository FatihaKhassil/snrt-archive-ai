import httpx


class LLMService:

    def __init__(self):

        self.url = "http://ollama:11434/api/generate"

        self.model = "llama3.2:3b"

    async def generate(

        self,

        prompt

    ):

        async with httpx.AsyncClient(

            timeout=300

        ) as client:

            response = await client.post(

                self.url,

                json={

                    "model": self.model,

                    "prompt": prompt,

                    "stream": False,

                    "options": {

                        "temperature": 0,

                        "top_p": 0.9,

                        "num_predict": 180,

                        "repeat_penalty": 1.1

                    }

                }

            )

        print(
            "Status:",
            response.status_code,
            flush=True
        )

        print(
            "Response:",
            response.text,
            flush=True
        )

        response.raise_for_status()

        data = response.json()

        return data["response"].strip()