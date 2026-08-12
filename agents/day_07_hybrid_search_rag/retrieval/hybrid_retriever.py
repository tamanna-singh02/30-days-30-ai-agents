from config import settings

from ingestion.vector_store import VectorStore
from retrieval.retriever import (
    Retriever,
    RetrievedDocument,
)

from indexing.bm25_index import BM25Index
from fusion.rrf import reciprocal_rank_fusion


class HybridRetriever:
    """
    Hybrid retriever combining:

    1. Dense vector retrieval
    2. Sparse BM25 retrieval
    3. Reciprocal Rank Fusion
    """

    def __init__(
        self,
        vector_store: VectorStore | None = None,
    ):
        self.vector_store = (
            vector_store
            or VectorStore()
        )

        self.dense_retriever = Retriever(
            vector_store=self.vector_store
        )

        documents = self.vector_store.get_documents()
        if not documents:
            if settings.DOCUMENTS_DIR.exists():
                from ingestion.chunker import Chunker
                from ingestion.loader import load_document

                all_chunks = []
                chunker = Chunker(strategy="recursive")

                for doc_file in settings.DOCUMENTS_DIR.glob("*"):
                    if doc_file.suffix.lower() in (
                        ".pdf",
                        ".md",
                        ".txt",
                        ".markdown",
                    ):
                        raw_docs = load_document(doc_file)
                        chunks = chunker.split_documents(raw_docs)
                        all_chunks.extend(chunks)

                if all_chunks:
                    self.vector_store.add_documents(all_chunks)
                    documents = self.vector_store.get_documents()

        self.bm25_index = BM25Index(documents=documents)



    def retrieve(
        self,
        query: str,
        k: int | None = None,
    ) -> list[RetrievedDocument]:

        retrieval_k = (
            k
            if k is not None
            else settings.RETRIEVAL_K
        )

        # --------------------------------
        # Dense Retrieval
        # --------------------------------

        dense_results = (
            self.dense_retriever.retrieve(
                query=query,
                k=retrieval_k,
            )
        )

        dense_results_for_rrf = []

        for rank, result in enumerate(
            dense_results,
            start=1,
        ):
            dense_results_for_rrf.append(
                {
                    "document": result.document,
                    "score": result.score,
                    "rank": rank,
                }
            )

        # --------------------------------
        # BM25 Retrieval
        # --------------------------------

        bm25_results = (
            self.bm25_index.search(
                query=query,
                k=retrieval_k,
            )
        )

        # --------------------------------
        # RRF
        # --------------------------------

        fused_results = reciprocal_rank_fusion(
            [
                dense_results_for_rrf,
                bm25_results,
            ]
        )

        # --------------------------------
        # Convert RRF results into the
        # same format used by Day 6
        # --------------------------------

        return [
            RetrievedDocument(
                document=result["document"],
                score=result["score"],
            )
            for result in fused_results[:retrieval_k]
        ]