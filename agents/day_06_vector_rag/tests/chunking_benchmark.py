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

from config import settings
from ingestion.chunker import Chunker
from ingestion.loader import load_document
from ingestion.vector_store import VectorStore
from retrieval.retriever import Retriever
from tests.evaluation_dataset import (
    EVALUATION_DATASET,
)
from tests.evaluator import RAGEvaluator


console = Console()

PDF_PATH = settings.DOCUMENTS_DIR / "report.pdf"


CONFIGURATIONS = [
    ("recursive", 300, 50),
    ("recursive", 500, 100),
    ("recursive", 800, 100),
    ("recursive", 1000, 200),
    ("token", 300, 50),
    ("token", 500, 50),
    ("token", 800, 100),
]


def benchmark_configuration(
    strategy: str,
    chunk_size: int,
    chunk_overlap: int,
):

    documents = load_document(
        PDF_PATH
    )

    chunker = Chunker(
        strategy=strategy,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = chunker.split_documents(
        documents
    )

    collection_name = (
        f"eval_"
        f"{strategy}_"
        f"{chunk_size}_"
        f"{chunk_overlap}"
    )

    vector_store = VectorStore(
        collection_name=collection_name
    )

    vector_store.reset()

    vector_store.add_documents(
        chunks
    )

    retriever = Retriever(
        vector_store=vector_store
    )

    evaluator = RAGEvaluator(
        retriever=retriever
    )

    metrics = evaluator.evaluate_dataset(
        dataset=EVALUATION_DATASET,
        k=5,
    )

    statistics = (
        chunker.get_statistics(
            chunks
        )
    )

    return {
        "strategy": strategy,
        "chunk_size": chunk_size,
        "overlap": chunk_overlap,
        "chunks": statistics[
            "total_chunks"
        ],
        "avg_length": statistics[
            "average_length"
        ],
        "precision": metrics[
            "precision_at_k"
        ],
        "recall": metrics[
            "recall_at_k"
        ],
        "mrr": metrics["mrr"],
        "success": metrics[
            "retrieval_success_rate"
        ],
    }


def main():

    console.print(
        "\n[bold cyan]"
        "Chunking Strategy Benchmark"
        "[/bold cyan]\n"
    )

    results = []

    for configuration in CONFIGURATIONS:

        strategy, size, overlap = (
            configuration
        )

        console.print(
            f"Testing "
            f"{strategy} "
            f"{size}/{overlap}..."
        )

        result = benchmark_configuration(
            strategy=strategy,
            chunk_size=size,
            chunk_overlap=overlap,
        )

        results.append(result)

    table = Table()

    table.add_column("Strategy")
    table.add_column("Size")
    table.add_column("Overlap")
    table.add_column("Chunks")
    table.add_column("Avg")
    table.add_column("P@5")
    table.add_column("R@5")
    table.add_column("MRR")
    table.add_column("Success")

    for result in results:

        table.add_row(
            result["strategy"],
            str(result["chunk_size"]),
            str(result["overlap"]),
            str(result["chunks"]),
            f'{result["avg_length"]:.1f}',
            f'{result["precision"]:.3f}',
            f'{result["recall"]:.3f}',
            f'{result["mrr"]:.3f}',
            f'{result["success"]:.3f}',
        )

    console.print("\n")
    console.print(table)


if __name__ == "__main__":
    main()