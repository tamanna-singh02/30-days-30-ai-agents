from dataclasses import dataclass

from langchain_core.documents import Document

from config import settings
from ingestion.vector_store import VectorStore


@dataclass
class RetrievedDocument:
    """
    Represents a retrieved document with its relevance score.
    """

    document: Document
    score: float


class Retriever:
    """
    Performs dense vector retrieval.
    """

    def __init__(
        self,
        vector_store: VectorStore | None = None,
    ):
        self.vector_store = (
            vector_store
            or VectorStore()
        )

    def retrieve(
        self,
        query: str,
        k: int | None = None,
    ) -> list[RetrievedDocument]:
        """
        Retrieve relevant documents using dense vector search.
        """

        retrieval_k = (
            k
            if k is not None
            else settings.RETRIEVAL_K
        )

        results = (
            self.vector_store
            .similarity_search_with_score(
                query=query,
                k=retrieval_k,
            )
        )

        retrieved = []

        for document, distance in results:


            #Chroma returns a distance.
            #Lower distance -> closer vector
            if(
                settings.SIMILARITY_THRESHOLD > 0
                and distance
                > settings.SIMILARITY_THRESHOLD
            ):
                continue

            retrieved.append(
                RetrievedDocument(
                    document=document,
                    score=float(distance),
                )
            )

        return retrieved

    def retrieve_documents(
        self,
        query: str,
        k: int | None = None,
    ) -> list[Document]:
        """
        Return only documents.
        """

        results = self.retrieve(
            query=query,
            k=k,
        )

        return [
            result.document
            for result in results
        ]