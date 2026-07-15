from app.services.solr_service import SolrService
from app.repositories.document_repository import DocumentRepository


class SearchService:

    def __init__(self):

        self.solr = SolrService()

        self.repository = DocumentRepository()

    async def keyword_search(

        self,

        keyword

    ):

        print(
            f"🔍 Keyword: {keyword}",
            flush=True
        )

        ids = await self.solr.search(

            keyword

        )

        print(
            f"📄 IDs returned by Solr: {ids}",
            flush=True
        )

        if not ids:

            print(
                "❌ No document found in Solr",
                flush=True
            )

            return []

        documents = await self.repository.get_documents(

            ids

        )

        print(
            f"📚 Documents returned by MongoDB: {len(documents)}",
            flush=True
        )

        return documents