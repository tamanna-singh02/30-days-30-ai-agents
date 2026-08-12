import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set

BASE_DIR = Path(__file__).resolve().parent.parent
DAY06_DIR = BASE_DIR.parent / "day_06_vector_rag"
ROOT_DIR = BASE_DIR.parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(DAY06_DIR) not in sys.path:
    sys.path.insert(0, str(DAY06_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import config

from indexing.bm25_index import BM25Index
from ingestion.vector_store import VectorStore
from retrieval.hybrid_pipeline import HybridSearchPipeline
from retrieval.hybrid_retriever import HybridRetriever
from retrieval.reranker import Reranker
from retrieval.retriever import Retriever
from rich.console import Console
from rich.table import Table

console = Console()

# -------------------------------------------------------------------
# Benchmark Ground Truth Dataset (Matching Ingested Documents)
# -------------------------------------------------------------------
BENCHMARK_DATASET = [
    {
        "query": "What is RAGAS evaluation framework and what does it measure?",
        "category": "exact",
        "relevant_chunk_keywords": ["ragas", "faithfulness", "precision"],
    },
    {
        "query": "What are the three real problems created when an LLM takes a closed-book exam?",
        "category": "semantic",
        "relevant_chunk_keywords": ["knowledge cutoff", "private", "hallucination"],
    },
    {
        "query": "How does Reciprocal Rank Fusion (RRF) calculate document scores?",
        "category": "hybrid",
        "relevant_chunk_keywords": ["rrf", "rank", "1 / (k + rank)"],
    },
    {
        "query": "What is the difference between open-book and closed-book exams for LLMs?",
        "category": "semantic",
        "relevant_chunk_keywords": ["open-book", "closed-book", "textbook"],
    },
    {
        "query": "What daily metrics including calories and weight are recorded in the report?",
        "category": "hybrid",
        "relevant_chunk_keywords": ["calories", "protein", "weight", "gym"],
    },
    {
        "query": "What environment variable configures the Redis cluster connection string REDIS_URL?",
        "category": "exact_token",
        "relevant_chunk_keywords": ["REDIS_URL", "secret_pass", "6379"],
    },
    {
        "query": "What secret key JWT_SECRET is used for signing access tokens?",
        "category": "exact_token",
        "relevant_chunk_keywords": ["JWT_SECRET", "super_secret_jwt_token_key_2026_prod"],
    },
    {
        "query": "When does the API gateway return a 401 Unauthorized error response?",
        "category": "exact_token",
        "relevant_chunk_keywords": ["401 Unauthorized", "Bearer token", "JWT_SECRET"],
    },
    {
        "query": "What is the endpoint /api/v1/auth/token used for?",
        "category": "exact_token",
        "relevant_chunk_keywords": ["/api/v1/auth/token", "access token"],
    },
]



@dataclass
class EvaluationMetrics:
    precision_at_5: float
    recall_at_5: float
    mrr: float
    success_rate: float
    avg_latency_ms: float


def check_relevance(doc_text: str, keywords: List[str]) -> bool:
    """Determine if a retrieved document chunk is relevant based on keywords."""
    text_lower = doc_text.lower()
    return any(kw.lower() in text_lower for kw in keywords)


def run_benchmark():
    console.print("\n[bold cyan]============================================================[/bold cyan]")
    console.print("[bold cyan]       BENCHMARK: DAY 6 (DENSE) vs DAY 7 (HYBRID RAG)       [/bold cyan]")
    console.print("[bold cyan]============================================================[/bold cyan]\n")

    vector_store = VectorStore()
    vector_store.reset()

    from ingestion.chunker import Chunker
    from ingestion.loader import load_document

    chunker = Chunker(strategy="recursive")
    for doc_file in config.settings.DOCUMENTS_DIR.glob("*"):
        if doc_file.suffix.lower() in (".pdf", ".md", ".txt", ".markdown"):
            chunks = chunker.split_documents(load_document(doc_file))
            vector_store.add_documents(chunks)

    documents = vector_store.get_documents()
    console.print(f"[green]Ingested {len(documents)} total chunks into VectorStore.[/green]")

    dense_retriever = Retriever(vector_store=vector_store)
    reranker = Reranker()
    hybrid_pipeline = HybridSearchPipeline()
    bm25_index = BM25Index(documents=documents)

    day6_precisions, day6_recalls, day6_mrrs, day6_successes = [], [], [], []
    day7_precisions, day7_recalls, day7_mrrs, day7_successes = [], [], [], []

    # Latency tracking (in ms)
    latency_dense_list = []
    latency_bm25_list = []
    latency_rrf_list = []
    latency_cross_encoder_list = []
    latency_day6_total_list = []
    latency_day7_total_list = []

    category_results: Dict[str, Dict[str, List[float]]] = {
        "semantic": {"day6_acc": [], "day7_acc": []},
        "exact": {"day6_acc": [], "day7_acc": []},
        "hybrid": {"day6_acc": [], "day7_acc": []},
        "exact_token": {"day6_acc": [], "day7_acc": []},
    }

    for idx, item in enumerate(BENCHMARK_DATASET, start=1):
        query = item["query"]
        category = item["category"]
        keywords = item["relevant_chunk_keywords"]

        console.print(f"[bold yellow]------------------------------------------------------------[/bold yellow]")
        console.print(f"[bold yellow]QUERY {idx} ({category.upper()}): {query}[/bold yellow]")
        console.print(f"[bold yellow]------------------------------------------------------------[/bold yellow]")

        # -------------------------------------------------------------------
        # DAY 6 BENCHMARK EXECUTION
        # -------------------------------------------------------------------
        t0 = time.perf_counter()
        dense_results = dense_retriever.retrieve(query=query, k=20)
        t_dense_end = time.perf_counter()

        day6_reranked = reranker.rerank(query=query, documents=dense_results, top_k=5)
        t_day6_end = time.perf_counter()

        day6_latency = (t_day6_end - t0) * 1000.0
        latency_day6_total_list.append(day6_latency)

        # -------------------------------------------------------------------
        # DAY 7 BENCHMARK EXECUTION WITH STAGE TIMINGS
        # -------------------------------------------------------------------
        t_d7_start = time.perf_counter()

        t_d_start = time.perf_counter()
        d_cand = dense_retriever.retrieve(query=query, k=20)
        t_d_end = time.perf_counter()
        d_time = (t_d_end - t_d_start) * 1000.0

        t_b_start = time.perf_counter()
        b_cand = bm25_index.search(query=query, k=20)
        t_b_end = time.perf_counter()
        b_time = (t_b_end - t_b_start) * 1000.0

        t_rrf_start = time.perf_counter()
        d_cand_rrf = [{"document": r.document, "score": r.score, "rank": i} for i, r in enumerate(d_cand, start=1)]
        from fusion.rrf import reciprocal_rank_fusion
        fused = reciprocal_rank_fusion([d_cand_rrf, b_cand])
        t_rrf_end = time.perf_counter()
        rrf_time = (t_rrf_end - t_rrf_start) * 1000.0

        t_ce_start = time.perf_counter()
        from retrieval.retriever import RetrievedDocument
        fused_retrieved = [RetrievedDocument(document=f["document"], score=f["score"]) for f in fused[:20]]
        day7_reranked = reranker.rerank(query=query, documents=fused_retrieved, top_k=5)
        t_ce_end = time.perf_counter()
        ce_time = (t_ce_end - t_ce_start) * 1000.0

        day7_latency = (t_ce_end - t_d7_start) * 1000.0

        latency_dense_list.append(d_time)
        latency_bm25_list.append(b_time)
        latency_rrf_list.append(rrf_time)
        latency_cross_encoder_list.append(ce_time)
        latency_day7_total_list.append(day7_latency)

        # -------------------------------------------------------------------
        # DEBUG OUTPUT PRINTING
        # -------------------------------------------------------------------
        console.print("[dim]DENSE RESULTS (Top 3):[/dim]")
        for r in d_cand[:3]:
            cid = r.document.metadata.get("chunk_id", "unk")
            console.print(f"  • {cid} (dist: {r.score:.4f})")

        console.print("[dim]BM25 RESULTS (Top 3):[/dim]")
        for r in b_cand[:3]:
            cid = r["document"].metadata.get("chunk_id", "unk")
            console.print(f"  • {cid} (score: {r['score']:.4f})")

        console.print("[dim]RRF FUSED CANDIDATES (Top 3):[/dim]")
        for r in fused[:3]:
            cid = r["document"].metadata.get("chunk_id", "unk")
            console.print(f"  • {cid} (rrf score: {r['score']:.4f})")

        console.print("[bold green]CROSS-ENCODER FINAL RESULTS (Day 7 Top 5):[/bold green]")
        for rank, r in enumerate(day7_reranked, start=1):
            cid = r.document.metadata.get("chunk_id", "unk")
            console.print(f"  {rank}. {cid} (CrossEncoder Score: {r.score:.4f})")

        # -------------------------------------------------------------------
        # METRIC CALCULATIONS
        # -------------------------------------------------------------------
        # Day 6 Metrics
        d6_relevant_count = sum(1 for item in day6_reranked if check_relevance(item.document.page_content, keywords))
        d6_precision = d6_relevant_count / 5.0
        d6_recall = 1.0 if d6_relevant_count > 0 else 0.0
        d6_mrr = 0.0
        for rank, item in enumerate(day6_reranked, start=1):
            if check_relevance(item.document.page_content, keywords):
                d6_mrr = 1.0 / rank
                break
        d6_success = 1.0 if d6_relevant_count > 0 else 0.0

        # Day 7 Metrics
        d7_relevant_count = sum(1 for item in day7_reranked if check_relevance(item.document.page_content, keywords))
        d7_precision = d7_relevant_count / 5.0
        d7_recall = 1.0 if d7_relevant_count > 0 else 0.0
        d7_mrr = 0.0
        for rank, item in enumerate(day7_reranked, start=1):
            if check_relevance(item.document.page_content, keywords):
                d7_mrr = 1.0 / rank
                break
        d7_success = 1.0 if d7_relevant_count > 0 else 0.0

        day6_precisions.append(d6_precision)
        day6_recalls.append(d6_recall)
        day6_mrrs.append(d6_mrr)
        day6_successes.append(d6_success)

        day7_precisions.append(d7_precision)
        day7_recalls.append(d7_recall)
        day7_mrrs.append(d7_mrr)
        day7_successes.append(d7_success)

        category_results[category]["day6_acc"].append(d6_recall)
        category_results[category]["day7_acc"].append(d7_recall)

        console.print(f"[cyan]Day 6 P@5: {d6_precision*100:.1f}%, MRR: {d6_mrr:.2f} | Day 7 P@5: {d7_precision*100:.1f}%, MRR: {d7_mrr:.2f}[/cyan]\n")

    # -------------------------------------------------------------------
    # LATENCY BREAKDOWN REPORT
    # -------------------------------------------------------------------
    avg_dense_t = sum(latency_dense_list) / len(latency_dense_list)
    avg_bm25_t = sum(latency_bm25_list) / len(latency_bm25_list)
    avg_rrf_t = sum(latency_rrf_list) / len(latency_rrf_list)
    avg_ce_t = sum(latency_cross_encoder_list) / len(latency_cross_encoder_list)
    avg_day7_t = sum(latency_day7_total_list) / len(latency_day7_total_list)

    console.print("\n[bold cyan]============================================================[/bold cyan]")
    console.print("[bold cyan]                 LATENCY BREAKDOWN (STAGES)                 [/bold cyan]")
    console.print("[bold cyan]============================================================[/bold cyan]")
    console.print(f"Dense Retrieval      : {avg_dense_t:6.2f} ms")
    console.print(f"BM25 Retrieval       : {avg_bm25_t:6.2f} ms")
    console.print(f"RRF Fusion            : {avg_rrf_t:6.2f} ms")
    console.print(f"Cross Encoder        : {avg_ce_t:6.2f} ms")
    console.print("--------------------------------")
    console.print(f"Total Pipeline       : {avg_day7_t:6.2f} ms\n")

    # -------------------------------------------------------------------
    # SUMMARY COMPARISON TABLE
    # -------------------------------------------------------------------
    summary_table = Table(title="BENCHMARK COMPARISON: DAY 6 vs DAY 7")
    summary_table.add_column("Metric", style="bold yellow")
    summary_table.add_column("Day 6 (Dense)", style="red", justify="right")
    summary_table.add_column("Day 7 (Hybrid RAG)", style="bold green", justify="right")
    summary_table.add_column("Improvement Delta", style="bold magenta", justify="right")

    p6 = (sum(day6_precisions) / len(day6_precisions)) * 100.0
    p7 = (sum(day7_precisions) / len(day7_precisions)) * 100.0
    summary_table.add_row("Precision@5", f"{p6:.1f}%", f"{p7:.1f}%", f"+{p7-p6:.1f}%")

    r6 = (sum(day6_recalls) / len(day6_recalls)) * 100.0
    r7 = (sum(day7_recalls) / len(day7_recalls)) * 100.0
    summary_table.add_row("Recall@5", f"{r6:.1f}%", f"{r7:.1f}%", f"+{r7-r6:.1f}%")

    mrr6 = sum(day6_mrrs) / len(day6_mrrs)
    mrr7 = sum(day7_mrrs) / len(day7_mrrs)
    summary_table.add_row("MRR (Mean Reciprocal Rank)", f"{mrr6:.3f}", f"{mrr7:.3f}", f"+{mrr7-mrr6:.3f}")

    sr6 = (sum(day6_successes) / len(day6_successes)) * 100.0
    sr7 = (sum(day7_successes) / len(day7_successes)) * 100.0
    summary_table.add_row("Retrieval Success Rate", f"{sr6:.1f}%", f"{sr7:.1f}%", f"+{sr7-sr6:.1f}%")

    l6 = sum(latency_day6_total_list) / len(latency_day6_total_list)
    summary_table.add_row("Average Latency (ms)", f"{l6:.1f} ms", f"{avg_day7_t:.1f} ms", f"+{avg_day7_t-l6:.1f} ms")

    console.print(summary_table)

    # -------------------------------------------------------------------
    # CATEGORY BREAKDOWN TABLE
    # -------------------------------------------------------------------
    cat_table = Table(title="PER-CATEGORY ACCURACY COMPARISON")
    cat_table.add_column("Category", style="bold yellow")
    cat_table.add_column("Day 6 Recall", style="red", justify="right")
    cat_table.add_column("Day 7 Recall", style="bold green", justify="right")
    cat_table.add_column("Gain", style="bold magenta", justify="right")

    for cat, data in category_results.items():
        c6 = (sum(data["day6_acc"]) / len(data["day6_acc"])) * 100.0 if data["day6_acc"] else 0.0
        c7 = (sum(data["day7_acc"]) / len(data["day7_acc"])) * 100.0 if data["day7_acc"] else 0.0
        gain = c7 - c6
        cat_table.add_row(cat.upper(), f"{c6:.1f}%", f"{c7:.1f}%", f"+{gain:.1f}%")

    console.print(cat_table)


if __name__ == "__main__":
    run_benchmark()
