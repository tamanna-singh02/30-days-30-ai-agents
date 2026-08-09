from dataclasses import dataclass
from langchain_core.documents import Document

from retrieval.retriever import RetrievedDocument


@dataclass
class RerankedDocument:
    document: Document
    score: float


class Reranker:
    """
    Reranks retrieved documents.

    For the initial implementation, we use the vector similarity distance.
    A CrossEncoder can be plugged in later.
    """

    def rerank(
        self,
        query: str,
        documents: list[RetrievedDocument],
        top_k: int | None = None,
    ) -> list[RerankedDocument]:
        if not documents:
            return []

        # Chroma returns distance: lower distance means higher relevance
        sorted_documents = sorted(
            documents,
            key=lambda item: item.score,
        )

        if top_k:
            sorted_documents = sorted_documents[:top_k]

        return [
            RerankedDocument(
                document=item.document,
                score=item.score,
            )
            for item in sorted_documents
        ]