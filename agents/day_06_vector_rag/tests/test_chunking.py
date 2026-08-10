import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

from config import settings
from ingestion.chunker import Chunker
from ingestion.loader import load_document


PDF_PATH = settings.DOCUMENTS_DIR / "report.pdf"


def test_recursive_chunking():

    documents = load_document(
        PDF_PATH
    )

    chunker = Chunker(
        strategy="recursive",
        chunk_size=500,
        chunk_overlap=100,
    )

    chunks = chunker.split_documents(
        documents
    )

    assert len(chunks) > 0

    statistics = (
        chunker.get_statistics(
            chunks
        )
    )

    assert (
        statistics["total_chunks"] > 0
    )

def benchmark_chunking():

    documents = load_document(
        PDF_PATH
    )

    configurations = [
        ("recursive", 300, 50),
        ("recursive", 500, 100),
        ("recursive", 800, 100),
        ("recursive", 1000, 200),
        ("token", 300, 50),
        ("token", 500, 50),
        ("token", 800, 100),
    ]

    print(
        "\n"
        + "=" * 80
    )

    print(
        "CHUNKING STRATEGY BENCHMARK"
    )

    print(
        "=" * 80
    )

    for strategy, size, overlap in configurations:

        chunker = Chunker(
            strategy=strategy,
            chunk_size=size,
            chunk_overlap=overlap,
        )

        chunks = chunker.split_documents(
            documents
        )

        stats = (
            chunker.get_statistics(
                chunks
            )
        )

        print(
            f"\n"
            f"Strategy: {strategy}\n"
            f"Chunk size: {size}\n"
            f"Overlap: {overlap}\n"
            f"Total chunks: "
            f"{stats['total_chunks']}\n"
            f"Average length: "
            f"{stats['average_length']}\n"
        )


if __name__ == "__main__":
    benchmark_chunking()