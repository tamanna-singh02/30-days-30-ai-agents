from typing import Iterable


def precision_at_k(
    retrieved_pages: list[int],
    relevant_pages: Iterable[int],
    k: int,
) -> float:
    """
    Precision@K:

    Of the top K retrieved results,
    how many were relevant?
    """

    relevant_pages = set(relevant_pages)

    top_k = retrieved_pages[:k]

    if not top_k:
        return 0.0

    relevant_count = sum(
        1
        for page in top_k
        if page in relevant_pages
    )

    return relevant_count / len(top_k)


def recall_at_k(
    retrieved_pages: list[int],
    relevant_pages: Iterable[int],
    k: int,
) -> float:
    """
    Recall@K:

    Of all relevant pages,
    how many were retrieved in top K?
    """

    relevant_pages = set(relevant_pages)

    if not relevant_pages:
        return 0.0

    top_k = set(
        retrieved_pages[:k]
    )

    retrieved_relevant = (
        top_k & relevant_pages
    )

    return (
        len(retrieved_relevant)
        / len(relevant_pages)
    )


def reciprocal_rank(
    retrieved_pages: list[int],
    relevant_pages: Iterable[int],
) -> float:
    """
    Reciprocal Rank:

    1 / rank of the first relevant result.
    """

    relevant_pages = set(relevant_pages)

    for rank, page in enumerate(
        retrieved_pages,
        start=1,
    ):
        if page in relevant_pages:
            return 1.0 / rank

    return 0.0


def mean_reciprocal_rank(
    results: list[float],
) -> float:
    """
    MRR across multiple queries.
    """

    if not results:
        return 0.0

    return sum(results) / len(results)


def retrieval_success(
    retrieved_pages: list[int],
    relevant_pages: Iterable[int],
    k: int,
) -> bool:
    """
    Returns True if at least one relevant page
    appears in the top K results.
    """

    relevant_pages = set(relevant_pages)

    return any(
        page in relevant_pages
        for page in retrieved_pages[:k]
    )
