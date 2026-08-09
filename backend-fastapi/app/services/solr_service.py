import requests


class SolrService:

    def __init__(self):

        self.url = (
            "http://solr:8983/solr/snrt_documents/select"
        )

        self.update_url = (
            "http://solr:8983/solr/snrt_documents/update"
        )

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

        results = response.json()[
            "response"
        ]["docs"]

        return [
            doc["id"]
            for doc in results
        ]

    async def delete_by_document_id(
        self,
        document_id: str
    ):

        response = requests.post(
            self.update_url,
            params={
                "commit": "true"
            },
            json={
                "delete": {
                    "id": document_id
                }
            }
        )

        response.raise_for_status()

        print(
            f"✅ Solr : document {document_id} supprimé",
            flush=True
        )