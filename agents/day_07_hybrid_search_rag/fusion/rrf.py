from collections import defaultdict


def reciprocal_rank_fusion(
    results_lists: list[list[dict]],
    k: int = 60,
) -> list[dict]:
    """
    Reciprocal Rank Fusion (RRF) algorithm to combine rank scores
    from multiple retrieval methods (e.g. Dense vector + BM25 sparse).
    RRF score = sum_i(1 / (k + rank_i))
    """
    scores = defaultdict(float)
    documents = {}

    for res_list in results_lists:
        for rank, result in enumerate(res_list, start=1):
            document = result["document"]
            doc_id = document.metadata.get(
                "chunk_id", str(hash(document.page_content))
            )
            scores[doc_id] += 1 / (k + rank)
            documents[doc_id] = document

    ranked_documents = sorted(
        scores.items(), key=lambda x: x[1], reverse=True
    )

    return [
        {
            "document": documents[doc_id],
            "score": score,
            "rank": rank,
        }
        for rank, (doc_id, score) in enumerate(ranked_documents, start=1)
    ]