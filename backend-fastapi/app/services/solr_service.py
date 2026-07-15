import requests


class SolrService:

    def __init__(self):

        self.url = "http://solr:8983/solr/snrt_documents/select"

    async def search(

        self,

        keyword

    ):

        response = requests.get(

            self.url,

            params={

                "defType": "edismax",

                "q": keyword,

                "qf": "title^5 summary^3 keywords^2 transcription",

                "fl": "id,score",

                "rows": 20,

                "wt": "json"

            }

        )

        response.raise_for_status()

        results = response.json()["response"]["docs"]

        return [

            doc["id"]

            for doc in results

        ]