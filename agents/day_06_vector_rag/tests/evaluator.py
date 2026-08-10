from dataclasses import dataclass

from retrieval.retriever import Retriever

from tests.evaluation_metrics import (
    mean_reciprocal_rank,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
    retrieval_success,
)


@dataclass
class EvaluationResult:
    question: str
    precision: float
    recall: float
    reciprocal_rank: float
    success: bool
    retrieved_pages: list[int]


class RAGEvaluator:

    def __init__(
        self,
        retriever: Retriever,
    ):
        self.retriever = retriever

    def evaluate_query(
        self,
        question: str,
        relevant_pages: list[int],
        k: int,
    ) -> EvaluationResult:

        results = self.retriever.retrieve(
            query=question,
            k=k,
        )

        retrieved_pages = []

        for result in results:

            page = result.document.metadata.get(
                "page"
            )

            if isinstance(page, int):
                page += 1

            if page is not None:
                retrieved_pages.append(page)

        return EvaluationResult(
            question=question,
            precision=precision_at_k(
                retrieved_pages,
                relevant_pages,
                k,
            ),
            recall=recall_at_k(
                retrieved_pages,
                relevant_pages,
                k,
            ),
            reciprocal_rank=reciprocal_rank(
                retrieved_pages,
                relevant_pages,
            ),
            success=retrieval_success(
                retrieved_pages,
                relevant_pages,
                k,
            ),
            retrieved_pages=retrieved_pages,
        )

    def evaluate_dataset(
        self,
        dataset: list[dict],
        k: int,
    ) -> dict:

        results = []

        for item in dataset:

            result = self.evaluate_query(
                question=item["question"],
                relevant_pages=item[
                    "relevant_pages"
                ],
                k=k,
            )

            results.append(result)

        precisions = [
            result.precision
            for result in results
        ]

        recalls = [
            result.recall
            for result in results
        ]

        reciprocal_ranks = [
            result.reciprocal_rank
            for result in results
        ]

        successes = [
            result.success
            for result in results
        ]

        return {
            "results": results,
            "precision_at_k": (
                sum(precisions)
                / len(precisions)
                if precisions
                else 0.0
            ),
            "recall_at_k": (
                sum(recalls)
                / len(recalls)
                if recalls
                else 0.0
            ),
            "mrr": mean_reciprocal_rank(
                reciprocal_ranks
            ),
            "retrieval_success_rate": (
                sum(successes)
                / len(successes)
                if successes
                else 0.0
            ),
        }