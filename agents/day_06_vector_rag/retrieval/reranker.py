from dataclasses import dataclass
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder

from config import settings
from retrieval.retriever import RetrievedDocument


@dataclass
class RerankedDocument:
    document: Document
    score: float


class Reranker:
    """
    Cross-encoder based document reranker.

    Dense retrieval finds candidate documents quickly.
    The cross-encoder then evaluates the query and each
    candidate together for better relevance estimation.
    """

    def __init__(self, model_name: str | None = None):

        self.model_name = model_name or settings.RERANKER_MODEL

        self.model = CrossEncoder(self.model_name)

    def rerank(
        self,
        query: str,
        documents: list[RetrievedDocument],
        top_k: int | None = None,
    ) -> list[RerankedDocument]:
        if not documents:
            return []

        pairs = [
            (
                query,
                item.document.page_content,
            )
            for item in documents
        ]

        scores = self.model.predict(
            pairs
        )

        reranked = []

        for item, score in zip(
            documents, scores
        ):
            reranked.append(
                RerankedDocument(
                    document=item.document,
                    score=float(score),
                )
            )


        #CrossEncoder score:
        #higher = more relevant
        reranked.sort(
            key=lambda x: x.score,
            reverse=True,
        )

        if top_k is not None:
            reranked = reranked[:top_k]

        return reranked