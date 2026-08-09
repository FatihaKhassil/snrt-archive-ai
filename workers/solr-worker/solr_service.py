import requests


class SolrService:

    def __init__(self):

        self.base_url = (
            "http://solr:8983/solr/"
            "snrt_documents"
        )

        self.index_url = (
            f"{self.base_url}/update/json/docs"
        )

        self.update_url = (
            f"{self.base_url}/update"
        )


    def index_document(

        self,

        document

    ):

        response = requests.post(

            self.index_url,

            json=document,

            params={
                "commit": "true"
            }

        )

        response.raise_for_status()

        print(
            f"✅ Document indexé dans Solr : "
            f"{document.get('id')}",
            flush=True
        )


    def delete_by_document_id(

        self,

        document_id: str

    ):

        """
        Supprime complètement le document de Solr
        en utilisant le même ID que MongoDB.
        """

        response = requests.post(

            self.update_url,

            json={
                "delete": {
                    "id": str(document_id)
                }
            },

            params={
                "commit": "true"
            }

        )

        response.raise_for_status()

        print(
            f"🗑️ Document supprimé de Solr : "
            f"{document_id}",
            flush=True
        )


    def delete_all_by_document_id(

        self,

        document_id: str

    ):

        """
        Variante utilisant une requête Solr.
        Utile si plusieurs documents possèdent
        le même identifiant dans l'index.
        """

        response = requests.post(

            self.update_url,

            json={
                "delete": {
                    "query": (
                        f'id:"{str(document_id)}"'
                    )
                }
            },

            params={
                "commit": "true"
            }

        )

        response.raise_for_status()

        print(
            f"🗑️ Documents Solr supprimés "
            f"pour document_id : {document_id}",
            flush=True
        )