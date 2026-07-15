from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings


class ChromaService:

    def __init__(self):

        self.embeddings = OllamaEmbeddings(

            model="nomic-embed-text",

            base_url="http://ollama:11434"

        )

        self.vector_store = Chroma(

            collection_name="snrt_documents",

            embedding_function=self.embeddings,

            host="chroma",
            port=8000

        )


    def add_document(

        self,

        document_id,

        chunks

    ):

        documents = []

        for index, chunk in enumerate(chunks):

            documents.append(

                Document(

                    page_content=chunk,

                    metadata={

                        "document_id": document_id,

                        "chunk_index": index

                    }

                )

            )

        self.vector_store.add_documents(

            documents

        )
    def count_documents(self):

        return self.vector_store._collection.count()