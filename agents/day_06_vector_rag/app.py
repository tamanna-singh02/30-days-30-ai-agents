import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from rich.console import Console
from rich.markdown import Markdown

from config import settings
from graph.rag_graph import RAGGraph
from ingestion.chunker import Chunker
from ingestion.loader import load_document
from ingestion.vector_store import VectorStore

console = Console()
PDF_PATH = settings.DOCUMENTS_DIR / "report.pdf"


def ingest_document():
    """Load, chunk, and index the document with clean text output."""
    console.print("\n[bold cyan]Vector Document RAG Agent[/bold cyan]")
    console.print("[dim]Day 06 — LangGraph & ChromaDB System[/dim]\n")

    with console.status("[cyan]Loading and indexing document...[/cyan]"):
        documents = load_document(PDF_PATH)
        chunker = Chunker(strategy="recursive")
        chunks = chunker.split_documents(documents)
        stats = chunker.get_statistics(chunks)

        vector_store = VectorStore()
        vector_store.add_documents(chunks)
        total_vectors = vector_store.get_collection_count()

    console.print(f"[cyan]Document:[/cyan] {PDF_PATH.name} ([green]{len(documents)} pages[/green])")
    console.print(f"[cyan]Chunks:[/cyan] [green]{stats['total_chunks']}[/green] created (avg {stats['average_length']} chars)")
    console.print(f"[cyan]Vector DB:[/cyan] [green]{total_vectors}[/green] vectors stored\n")


def ask_questions():
    """Interactive Q&A loop with simple, elegant text formatting (no tables)."""
    with console.status("[cyan]Initializing RAG agent...[/cyan]"):
        rag = RAGGraph()

    while True:
        try:
            question = console.input("[bold cyan]Ask a question[/bold cyan] (type 'exit' to quit): ")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye.[/dim]")
            break

        cleaned = question.strip()
        if not cleaned:
            continue

        if cleaned.lower() in ("exit", "q", "quit"):
            console.print("\n[dim]Goodbye.[/dim]")
            break

        with console.status("[cyan]Searching documents...[/cyan]"):
            result = rag.invoke(cleaned)

        answer_text = result.get("answer", "No answer generated.")
        sources = result.get("sources", [])

        console.print("\n[bold green]Answer:[/bold green]")
        console.print(Markdown(answer_text))

        if sources:
            console.print("\n[bold cyan]Sources:[/bold cyan]")
            seen = set()
            for s in sources:
                key = (s["source"], s["page"])
                if key in seen:
                    continue
                seen.add(key)
                console.print(f"• [cyan]{s['source']}[/cyan] — Page [green]{s['page']}[/green]")

        console.print()


def main():
    if not PDF_PATH.exists():
        console.print(f"[red]PDF file not found at {PDF_PATH}[/red]")
        return

    ingest_document()
    ask_questions()


if __name__ == "__main__":
    main()