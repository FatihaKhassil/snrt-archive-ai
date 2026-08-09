from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


class ChromaService:

    def __init__(self):

        embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url="http://ollama:11434"
        )

        self.vector_store = Chroma(
            collection_name="snrt_documents",
            embedding_function=embeddings,
            host="chroma",
            port=8000
        )


    async def search(
        self,
        question,
        k=5
    ):

        return self.vector_store.similarity_search(
            query=question,
            k=k
        )


    async def delete_by_document_id(
        self,
        document_id: str
    ):

        document_id = str(document_id)

        print(
            f"🗑️ ChromaDB : suppression du document {document_id}",
            flush=True
        )

        self.vector_store.delete(
            where={
                "document_id": document_id
            }
        )

        print(
            f"✅ ChromaDB : document {document_id} supprimé",
            flush=True
        )