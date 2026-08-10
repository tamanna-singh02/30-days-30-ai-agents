import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from rich.console import Console
from rich.table import Table

from retrieval.retriever import Retriever
from tests.evaluation_dataset import (
    EVALUATION_DATASET,
)
from tests.evaluator import RAGEvaluator


console = Console()


def main():

    retriever = Retriever()

    evaluator = RAGEvaluator(
        retriever= retriever,
    )

    results = evaluator.evaluate_dataset(
        dataset=EVALUATION_DATASET,
        k=5,
    )

    console.print(
        "\n[bold cyan]RAG Evaluation[/bold cyan]\n"
    )

    table = Table()

    table.add_column("Question")
    table.add_column("Precision@5")
    table.add_column("Recall@5")
    table.add_column("RR")
    table.add_column("Success")
    table.add_column("Pages")

    for result in results["results"]:

        table.add_row(
            result.question[:40],
            f"{result.precision:.2f}",
            f"{result.recall:.2f}",
            f"{result.reciprocal_rank:.2f}",
            "Yes" if result.success else "No",
            str(result.retrieved_pages),
        )

    console.print(table)

    console.print(
        "\n[bold green]Overall Metrics[/bold green]"
    )

    console.print(
        f"Precision@5: "
        f"{results['precision_at_k']:.3f}"
    )

    console.print(
        f"Recall@5: "
        f"{results['recall_at_k']:.3f}"
    )

    console.print(
        f"MRR: "
        f"{results['mrr']:.3f}"
    )

    console.print(
        f"Retrieval Success Rate: "
        f"{results['retrieval_success_rate']:.3f}"
    )


if __name__ == "__main__":
    main()