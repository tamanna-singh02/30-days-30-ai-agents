import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from rich.console import Console

from rich.panel import Panel

from config import settings
from graph.rag_graph import RAGGraph
from ingestion.chunker import Chunker
from ingestion.loader import load_document
from ingestion.vector_store import VectorStore


console = Console()

PDF_PATH = settings.DOCUMENTS_DIR / "report.pdf"



def ingest_document():
    """
    Load, chunk and index the PDF.
    """

    console.print(
        "\n[bold cyan]📄 Loading document...[/bold cyan]"
    )

    documents = load_document(
        PDF_PATH
    )

    console.print(
        f"Loaded [green]{len(documents)}[/green] pages."
    )

    console.print(
        "\n[bold cyan]✂️ Chunking document...[/bold cyan]"
    )

    chunker = Chunker(
        strategy="recursive"
    )

    chunks = chunker.split_documents(
        documents
    )

    statistics = chunker.get_statistics(
        chunks
    )

    console.print(
        f"Created [green]{statistics['total_chunks']}[/green] chunks."
    )

    console.print(
        f"Average chunk length: "
        f"[yellow]{statistics['average_length']}[/yellow]"
    )

    console.print(
        "\n[bold cyan]🧠 Creating embeddings "
        "and storing vectors...[/bold cyan]"
    )

    vector_store = VectorStore()

    vector_store.add_documents(
        chunks
    )

    count = vector_store.get_collection_count()

    console.print(
        f"Vector database contains "
        f"[green]{count}[/green] vectors."
    )


def ask_questions():

    console.print(
        Panel(
            "Vector Document RAG Agent",
            title="🤖 Day 6",
        )
    )

    rag = RAGGraph()

    while True:

        question = console.input(
            "\n[bold cyan]Ask a question "
            "(type 'exit' to quit): [/bold cyan]"
        )

        if question.lower().strip() == "exit":
            break

        if not question.strip():
            continue

        console.print(
            "\n[yellow]🔎 Searching documents...[/yellow]"
        )

        result = rag.invoke(
            question
        )

        console.print(
            "\n[bold green]Answer:[/bold green]"
        )

        console.print(
            result.get(
                "answer",
                "No answer generated.",
            )
        )

        sources = result.get(
            "sources",
            [],
        )

        if sources:

            console.print(
                "\n[bold cyan]Sources:[/bold cyan]"
            )

            seen = set()

            for source in sources:

                key = (
                    source["source"],
                    source["page"],
                )

                if key in seen:
                    continue

                seen.add(key)

                console.print(
                    f"• {source['source']} "
                    f"— Page {source['page']}"
                )


def main():

    if not PDF_PATH.exists():

        console.print(
            f"[red]PDF not found: "
            f"{PDF_PATH}[/red]"
        )

        return

    ingest_document()

    ask_questions()


if __name__ == "__main__":
    main()