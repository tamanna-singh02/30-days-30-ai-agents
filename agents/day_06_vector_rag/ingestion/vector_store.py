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
        Add documents to the vector database and populate chunk_id in metadata.
        """
        if not documents:
            return []

        ids = []
        for index, document in enumerate(documents):
            doc_id = self._create_document_id(document, index)
            ids.append(doc_id)
            document.metadata["chunk_id"] = doc_id

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

    def get_documents(self) -> list[Document]:
        """
        Retrieve all documents stored in the Chroma collection, ensuring
        document.metadata['chunk_id'] is present.
        """
        collection_data = self.vector_store._collection.get(
            include=["documents", "metadatas"]
        )
        ids = collection_data.get("ids") or []
        contents = collection_data.get("documents") or []
        metadatas = collection_data.get("metadatas") or []

        documents = []
        for doc_id, content, metadata in zip(ids, contents, metadatas):
            meta = dict(metadata or {})
            if "chunk_id" not in meta or not meta["chunk_id"]:
                meta["chunk_id"] = doc_id
            documents.append(Document(page_content=content, metadata=meta))
        return documents


    def reset(self):
        """
        Delete all vectors from the current collection.
        """
        self.vector_store.delete_collection()

        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=embedder.get_embedding_model(),
            persist_directory=str(settings.VECTOR_DB_DIR),
        )


   