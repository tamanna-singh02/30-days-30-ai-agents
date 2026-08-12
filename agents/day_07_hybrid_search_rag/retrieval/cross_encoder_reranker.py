from dataclasses import dataclass

from langchain_core.documents import Document
from sentence_transformers import CrossEncoder


@dataclass
class RerankedDocument:
    document: Document
    score: float


class CrossEncoderReranker:

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
    ):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        documents: list[Document],
        top_k: int = 5,
    ) -> list[RerankedDocument]:

        if not documents:
            return []

        pairs = [
            (query, document.page_content)
            for document in documents
        ]

        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(documents, scores),
            key=lambda item: float(item[1]),
            reverse=True,
        )

        return [
            RerankedDocument(
                document=document,
                score=float(score),
            )
            for document, score in ranked[:top_k]
        ]