# Day 07 — Hybrid Search RAG Agent

An advanced Hybrid Search Retrieval-Augmented Generation (RAG) agent combining **Dense Vector Search (ChromaDB)** and **Sparse Lexical Search (BM25)** with **Reciprocal Rank Fusion (RRF)** and cross-encoder relevance re-ranking.

---

## 🏗️ Architecture

```text
                        User Query
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
     Dense Vector Search         Sparse Lexical Search
         (ChromaDB)                    (BM25)
              │                           │
              └─────────────┬─────────────┘
                            │
                            ▼
              ┌──────────────────────────┐
              │ Reciprocal Rank Fusion   │
              └─────────────┬────────────┘
                            │
                            ▼
              ┌──────────────────────────┐
              │ Cross-Encoder Re-ranker  │
              └─────────────┬────────────┘
                            │ (Top Reranked Context)
                            ▼
              ┌──────────────────────────┐
              │  LangGraph Answer Node   │
              └─────────────┬────────────┘
                            │
                            ▼
                     Grounded Answer
```

---

## ✨ Features

- ✅ **Hybrid Retrieval**: Combines semantic vector search (dense) and keyword exact match (sparse BM25).
- ✅ **Reciprocal Rank Fusion (RRF)**: Merges ranked results from multiple search streams without score normalization issues.
- ✅ **Cross-Encoder Re-ranking**: Re-scores top candidates to maximize context precision before LLM generation.
- ✅ **Evaluation & Benchmarking**: Includes benchmark suites comparing Vector-only vs. Hybrid retrieval accuracy.
- ✅ **LangGraph Workflow**: Pure state machine managing retrieval, fusion, re-ranking, and response generation.

---

## 📁 Project Structure

```text
day_07_hybrid_search_rag/
├── app.py                     # CLI Interactive Hybrid RAG Entrypoint
├── config.py                  # Search, Fusion & Reranking Settings
├── requirements.txt           # Agent-specific Dependencies
├── README.md                  # Project Documentation
├── evaluation/                # Benchmark Evaluation Pipeline
├── fusion/                    # Reciprocal Rank Fusion (RRF) Logic
├── graph/                     # LangGraph State Graph & Nodes
├── indexing/                  # Document Vector & BM25 Indexers
├── prompts/                   # System & Reranking Prompts
├── retrieval/                 # Dense & Sparse Retrievers
├── tests/                     # Test Suite & Performance Benchmarks
└── utils/                     # Cross-Encoder Reranker & Formatting
```

---

## 🚀 Usage

### Run Interactive Application

```bash
python agents/day_07_hybrid_search_rag/app.py
```

### Run Tests & Benchmarks

```bash
pytest agents/day_07_hybrid_search_rag/tests/
```
