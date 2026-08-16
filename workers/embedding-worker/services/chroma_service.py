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


    def add_document(
        self,
        document_id: str,
        chunks: list[str]
    ):

        document_id = str(document_id)

        print(
            f"🧠 Génération des embeddings pour {len(chunks)} chunks...",
            flush=True
        )

        metadatas = [
            {
                "document_id": document_id,
                "chunk_index": index
            }
            for index in range(len(chunks))
        ]

        self.vector_store.add_texts(
            texts=chunks,
            metadatas=metadatas
        )

        print(
            f"✅ {len(chunks)} chunks ajoutés à ChromaDB",
            flush=True
        )


    def count_documents(self):

        return self.vector_store._collection.count()