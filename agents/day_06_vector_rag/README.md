# Day 06 — Vector Document RAG Agent

A production-grade Vector Retrieval-Augmented Generation (RAG) agent built using **LangGraph**, **ChromaDB**, and **PyPDF**. It handles PDF document ingestion, configurable text chunking, dense vector similarity retrieval, and citation-backed question answering.

---

## 🏗️ Architecture

```text
               User Document / Query
                        │
                        ▼
          ┌──────────────────────────┐
          │   Document Ingestion     │
          │ (PDF Parsing & Chunking) │
          └─────────────┬────────────┘
                        │
                        ▼
          ┌──────────────────────────┐
          │   Chroma Vector Store    │ ◄── Dense Vector Search
          └─────────────┬────────────┘
                        │ (Retrieved Chunks)
                        ▼
          ┌──────────────────────────┐
          │     LangGraph State      │
          │   (Citation Synthesis)   │
          └─────────────┬────────────┘
                        │
                        ▼
               Answer with Citations
```

---

## ✨ Features

- ✅ **Document Ingestion & Chunking**: Extracts text from PDFs and splits into overlapping semantic chunks.
- ✅ **Dense Vector Search**: Powered by ChromaDB for fast similarity retrieval.
- ✅ **LangGraph Workflow**: Pure state-driven graph execution for prompt injection and context hydration.
- ✅ **Citations & Verification**: Attaches source metadata and page references to generated answers.
- ✅ **Resilient Embeddings**: Auto-selects OpenAI embeddings or local Chroma ONNX embeddings.

---

## 📁 Project Structure

```text
day_06_vector_rag/
├── app.py                     # CLI Interactive RAG Entrypoint
├── config.py                  # Chunking & Storage Settings
├── requirements.txt           # Agent-specific Dependencies
├── README.md                  # Project Documentation
├── database/                  # Chroma Vector Store Handler
├── documents/                 # Document Storage & Sample PDFs
├── graph/                     # LangGraph State Graph & Nodes
├── ingestion/                 # PDF Parsing & Chunking Utilities
├── prompts/                   # RAG System Prompts
├── retrieval/                 # Vector Store Retriever
├── tests/                     # Test Suite & Evaluation Scripts
└── utils/                     # Formatting & Benchmarking Helpers
```

---

## 🚀 Usage

### Run Interactive Application

```bash
python agents/day_06_vector_rag/app.py
```

### Run Tests

```bash
pytest agents/day_06_vector_rag/tests/
```
