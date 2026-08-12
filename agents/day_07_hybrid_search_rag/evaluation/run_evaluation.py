import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DAY06_DIR = BASE_DIR.parent / "day_06_vector_rag"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(DAY06_DIR) not in sys.path:
    sys.path.insert(0, str(DAY06_DIR))

from evaluation.evaluation_dataset import EVALUATION_DATASET
from graph.hybrid_rag_graph import HybridRAGGraph
from ingestion.vector_store import VectorStore
from retrieval.retriever import Retriever
from rich.console import Console
from rich.table import Table

console = Console()


def calculate_hit_rate(context: str, key_phrases: list[str]) -> float:
    """Calculate percentage of key ground truth phrases retrieved in context."""
    if not key_phrases:
        return 100.0
    context_lower = context.lower()
    found = sum(1 for phrase in key_phrases if phrase.lower() in context_lower)
    return (found / len(key_phrases)) * 100.0


def run_comparative_evaluation():
    console.print("\n[bold cyan]Production RAG Evaluation Benchmark[/bold cyan]")
    console.print(
        "[dim]Comparing Baseline Dense Search vs. Day 07 Hybrid Search (Dense + BM25 + RRF + Reranker)[/dim]\n"
    )

    vector_store = VectorStore()
    dense_retriever = Retriever(vector_store=vector_store)
    hybrid_agent = HybridRAGGraph()

    table = Table(title="Retrieval Recall & Accuracy Comparison")
    table.add_column("Query Type", style="bold yellow")
    table.add_column("Query", style="cyan")
    table.add_column("Dense Recall", style="red", justify="right")
    table.add_column("Hybrid Recall", style="bold green", justify="right")
    table.add_column("Delta Improvement", style="bold magenta", justify="right")

    dense_scores = []
    hybrid_scores = []

    for item in EVALUATION_DATASET:
        query = item["query"]
        q_type = item.get("query_type", "General")
        phrases = item.get("key_phrases", [])

        # 1. Dense Baseline (Top 5)
        dense_results = dense_retriever.retrieve(query=query, k=5)
        dense_ctx = "\n".join([r.document.page_content for r in dense_results])
        d_score = calculate_hit_rate(dense_ctx, phrases)
        dense_scores.append(d_score)

        # 2. Hybrid Search (Top 5)
        hybrid_res = hybrid_agent.invoke(query)
        hybrid_ctx = hybrid_res.get("context", "")
        h_score = calculate_hit_rate(hybrid_ctx, phrases)
        hybrid_scores.append(h_score)


        diff = h_score - d_score
        diff_str = f"+{diff:.1f}%" if diff > 0 else f"{diff:.1f}%"

        table.add_row(
            q_type,
            query[:45] + "..." if len(query) > 45 else query,
            f"{d_score:.1f}%",
            f"{h_score:.1f}%",
            diff_str,
        )

    console.print(table)

    avg_dense = sum(dense_scores) / len(dense_scores) if dense_scores else 0
    avg_hybrid = sum(hybrid_scores) / len(hybrid_scores) if hybrid_scores else 0
    total_gain = avg_hybrid - avg_dense

    console.print(f"[bold]Summary Benchmark Metrics:[/bold]")
    console.print(f" • Dense Vector Baseline Recall: [red]{avg_dense:.1f}%[/red]")
    console.print(f" • Hybrid Search (Day 07) Recall: [bold green]{avg_hybrid:.1f}%[/bold green]")
    console.print(
        f" • Overall Accuracy Improvement: [bold magenta]+{total_gain:.1f}%[/bold magenta]\n"
    )


if __name__ == "__main__":
    run_comparative_evaluation()


