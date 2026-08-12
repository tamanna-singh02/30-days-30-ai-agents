import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent.parent
DAY06_DIR = BASE_DIR.parent / "day_06_vector_rag"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(DAY06_DIR) not in sys.path:
    sys.path.insert(0, str(DAY06_DIR))
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
from graph.hybrid_rag_graph import HybridRAGGraph
from ingestion.chunker import Chunker
from ingestion.loader import load_document
from ingestion.vector_store import VectorStore

console = Console()


def ingest_documents():
    """Load, chunk, and index all documents in DOCUMENTS_DIR into VectorStore."""
    console.print("\n[bold cyan]Hybrid Search RAG Agent[/bold cyan]")
    console.print(
        "[dim]Day 07 — Dense Vector + BM25 Lexical + RRF + Cross-Encoder Reranker[/dim]\n"
    )

    doc_files = [
        f
        for f in settings.DOCUMENTS_DIR.glob("*")
        if f.suffix.lower() in (".pdf", ".md", ".txt", ".markdown")
    ]

    if not doc_files:
        console.print(
            f"[yellow]No documents found in {settings.DOCUMENTS_DIR}[/yellow]"
        )
        return

    vector_store = VectorStore()

    with console.status("[cyan]Ingesting and verifying document index...[/cyan]"):
        all_chunks = []
        chunker = Chunker(strategy="recursive")

        # Check existing collection
        existing_docs = vector_store.get_documents()
        existing_sources = {
            d.metadata.get("source") for d in existing_docs if d.metadata
        }

        new_files_ingested = 0
        for doc_file in doc_files:
            if doc_file.name not in existing_sources:
                raw_docs = load_document(doc_file)
                chunks = chunker.split_documents(raw_docs)
                vector_store.add_documents(chunks)
                new_files_ingested += 1

        total_vectors = vector_store.get_collection_count()

    console.print(
        f"[cyan]Active Documents:[/cyan] [green]{', '.join([f.name for f in doc_files])}[/green]"
    )
    if new_files_ingested > 0:
        console.print(
            f"[green]Successfully ingested {new_files_ingested} new document(s).[/green]"
        )
    console.print(
        f"[cyan]Vector DB:[/cyan] [green]{total_vectors}[/green] total vectors active\n"
    )


def ask_questions():
    """Interactive Q&A loop with hybrid retrieval."""
    with console.status("[cyan]Initializing Hybrid Search RAG agent...[/cyan]"):
        agent = HybridRAGGraph()

    console.print("[bold green]Agent ready! Ask your questions below.[/bold green]\n")

    while True:
        try:
            question = console.input(
                "[bold cyan]Ask a question[/bold cyan] (type 'exit' to quit): "
            )
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye.[/dim]")
            break

        cleaned = question.strip()
        if not cleaned:
            continue

        if cleaned.lower() in ("exit", "q", "quit"):
            console.print("\n[dim]Goodbye.[/dim]")
            break

        with console.status(
            "[cyan]Executing Hybrid Search (Dense + BM25 + RRF + Cross-Encoder)...[/cyan]"
        ):
            result = agent.invoke(cleaned)

        answer_text = result.get("answer", "No answer generated.")
        sources = result.get("sources", [])

        console.print("\n[bold green]Answer:[/bold green]")
        console.print(Markdown(answer_text))

        if sources:
            console.print("\n[bold cyan]Top Reranked Sources:[/bold cyan]")
            seen = set()
            for s in sources:
                page_info = (
                    f"Page {s['page']}"
                    if s["page"] != "unknown"
                    else "Full Document"
                )
                key = (s["source"], page_info)
                if key in seen:
                    continue
                seen.add(key)
                score_str = f" (Score: {s['score']:.4f})" if "score" in s else ""
                console.print(
                    f"• [cyan]{s['source']}[/cyan] — [green]{page_info}[/green]{score_str}"
                )

        console.print()


def main():
    ingest_documents()
    ask_questions()


if __name__ == "__main__":
    main()

