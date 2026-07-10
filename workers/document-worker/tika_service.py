import requests


class TikaService:

    def __init__(self):

        self.url = "http://tika:9998"

    def extract(self, file_path):

        with open(file_path, "rb") as file:

            response = requests.put(
                f"{self.url}/tika",
                data=file,
                headers={
                    "Accept": "text/plain; charset=UTF-8"
                }
            )

        response.raise_for_status()

        response.encoding = "utf-8"

        return response.text