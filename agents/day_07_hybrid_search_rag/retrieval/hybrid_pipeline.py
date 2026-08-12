from config import settings

from retrieval.hybrid_retriever import HybridRetriever
from retrieval.reranker import (
    Reranker,
    RerankedDocument,
)


class HybridSearchPipeline:
    """
    Complete Day 7 retrieval pipeline:

    Dense + BM25
          ↓
        RRF
          ↓
    Cross-Encoder
          ↓
        Top-K
    """

    def __init__(
        self,
        hybrid_retriever: HybridRetriever | None = None,
        reranker: Reranker | None = None,
    ):

        self.hybrid_retriever = (
            hybrid_retriever
            or HybridRetriever()
        )

        self.reranker = (
            reranker
            or Reranker()
        )

    def retrieve(
        self,
        query: str,
        candidate_k: int | None = None,
        final_k: int | None = None,
    ) -> list[RerankedDocument]:

        candidate_k = (
            candidate_k
            if candidate_k is not None
            else settings.RETRIEVAL_K
        )

        final_k = (
            final_k
            if final_k is not None
            else settings.TOP_K
        )

        # -----------------------------
        # Stage 1:
        # Dense + BM25 + RRF
        # -----------------------------

        candidates = (
            self.hybrid_retriever.retrieve(
                query=query,
                k=candidate_k,
            )
        )

        # -----------------------------
        # Stage 2:
        # Cross Encoder
        # -----------------------------

        reranked = self.reranker.rerank(
            query=query,
            documents=candidates,
            top_k=final_k,
        )

        return reranked