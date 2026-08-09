from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from config import settings
from ingestion.embedder import embedder


class VectorStore:
    """
    Persistent Chroma vector store.
    """

    def __init__(self, collection_name: str = "documents"):
        self.collection_name = collection_name
        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=embedder.get_embedding_model(),
            persist_directory=str(settings.VECTOR_DB_DIR),
        )

    def add_documents(self, documents: list[Document]) -> list[str]:
        """
        Add documents to the vector database.
        """
        if not documents:
            return []

        ids = [
            self._create_document_id(
                document,
                index,
            )
            for index, document in enumerate(documents)
        ]

        self.vector_store.add_documents(
            documents=documents,
            ids=ids,
        )

        return ids

    def similarity_search(self, query: str, k: int | None = None):
        """
        Perform dense vector similarity search.
        """
        k = k or settings.TOP_K
        return self.vector_store.similarity_search(query, k=k)

    def similarity_search_with_score(self, query: str, k: int | None = None):
        """
        Similarity search with distance scores.
        """
        k = k or settings.TOP_K
        return self.vector_store.similarity_search_with_score(query, k=k)

    def get_collection_count(self) -> int:
        """
        Return number of stored vectors.
        """
        collection = self.vector_store._collection
        return collection.count()

    @staticmethod
    def _create_document_id(document: Document, index: int) -> str:
        """
        Generate a deterministic-ish document ID.
        """
        source = document.metadata.get("source", "unknown")
        page = document.metadata.get("page", 0)
        chunk_index = document.metadata.get("chunk_index", index)

        return f"{source}:{page}:{chunk_index}"
