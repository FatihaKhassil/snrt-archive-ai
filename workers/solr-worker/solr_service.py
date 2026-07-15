import requests


class SolrService:

    def __init__(self):

        self.url = (

            "http://solr:8983/solr/"

            "snrt_documents/update/json/docs"

        )


    def index_document(

        self,

        document

    ):

        response = requests.post(

            self.url,

            json=document,

            params={

                "commit": "true"

            }

        )

        response.raise_for_status()