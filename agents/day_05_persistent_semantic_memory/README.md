# Day 5: Persistent Semantic Memory Agent

A dual-store long-term memory agent built using **LangGraph**, **ChromaDB**, and **SQLite**. It automatically extracts structured user facts and unstructured semantic memories from conversation streams, persists them across sessions, and retrieves relevant context for multi-turn AI interactions.

---

## 🏗️ Architecture

```
                      User Input
                          │
                          ▼
            ┌──────────────────────────┐
            │     retrieve_memory      │ ◄── Chroma Vector Store
            └─────────────┬────────────┘
                          │ (Retrieved Context)
                          ▼
            ┌──────────────────────────┐
            │        assistant         │ ───► Generates Answer
            └─────────────┬────────────┘
                          │
                          ▼
            ┌──────────────────────────┐
            │      extract_memory      │ ───► JSON Memory Extractor
            └─────────────┬────────────┘
                          │ (Extracted Entities)
                          ▼
            ┌──────────────────────────┐
            │       save_memory        │
            └──────────────┬───────────┘
                           │
            ┌──────────────┴──────────────┐
            ▼                             ▼
   SQLite (KV Store)            Chroma (Vector Store)
  (Structured Facts)           (Semantic Memories)
```

---

## ✨ Features

- ✅ **Dual-Store Memory Architecture**:
  - **Relational KV Store (SQLite)**: Stores exact key-value facts (Name, Project, Framework).
  - **Vector Store (ChromaDB)**: Performs similarity search across unstructured semantic memories.
- ✅ **Automatic Memory Extraction**: Parses user conversations using structured JSON schemas to capture identity, preferences, skills, and projects.
- ✅ **Context-Aware Retrieval**: Dynamically fetches relevant top-$k$ memories prior to LLM response generation.
- ✅ **Resilient Embedding Fallback**: Seamlessly uses **OpenAI Embeddings** (`text-embedding-3-small`) when an API key is available, or automatically falls back to free local **Chroma ONNX Embeddings** (`all-MiniLM-L6-v2`) when running offline without credentials.
- ✅ **LangGraph Workflow**: Pure state-driven graph orchestration with strict type guarantees.
- ✅ **Multi-Turn Persistence**: Database state survives across session restarts.

---

## 📁 Project Structure

```
day_05_persistent_semantic_memory/
├── app.py                     # CLI Interactive Chat Entrypoint
├── config.py                  # Environment & Directory Settings
├── requirements.txt           # Agent-specific Dependencies
├── README.md                  # Project Documentation
├── graphs/
│   ├── assistant_graph.py     # LangGraph Workflow Execution Graph
│   └── state.py               # AssistantState TypedDict Definition
├── memory/
│   ├── embeddings.py          # Embeddings Factory (OpenAI / Local Fallback)
│   ├── kv_store.py            # SQLite Relational Store (SQLAlchemy)
│   ├── memory_manager.py      # Dual-Store Memory Orchestrator
│   ├── schemas.py             # Memory & Category Pydantic Schemas
│   └── vector_store.py        # Chroma Vector Store Controller
├── nodes/
│   ├── assistant.py           # Core LLM Response Node
│   ├── extract_memory.py      # Conversation Memory Extraction Node
│   ├── retrieve_memory.py     # Context Retrieval Node
│   └── save_memory.py        # Dual-Store Saver Node
├── prompts/
│   ├── assistant.py           # Context-Injected System Prompt
│   └── extraction.py          # Memory Extraction System Prompt
└── data/
    ├── chroma/                # Chroma Vector Store Persistence Directory
    └── memory.db              # SQLite Database File
```

---

## 🚀 Usage

### 1. Interactive Chat Session

Start the interactive CLI app:

```bash
python agents/day_05_persistent_semantic_memory/app.py
```

### 2. Example Interaction

```text
Persistent Semantic Memory
---------------------------

You : Hi, my name is Tamanna. I am working on a 30-day AI agent challenge and my favorite framework is LangGraph.

Assistant:
Hello Tamanna, nice to meet you! That's exciting to hear about your 30-day AI agent challenge. LangGraph is a powerful framework to build stateful multi-actor applications. How can I assist you with your project today?

You : What is my favorite framework and what project am I working on?

Assistant:
Your favorite framework is LangGraph, and you're currently working on the 30-day AI agent challenge!
```

---

## ⚙️ Configuration & Environment

Configuration settings can be adjusted in `.env`:

```env
# Primary LLM Provider (groq, openai, google, anthropic)
MODEL_PROVIDER=groq
MODEL_NAME=llama-3.3-70b-versatile

# Optional: Embedding API Key (Leave empty to use local ONNX Chroma Embeddings)
OPENAI_API_KEY=your_openai_api_key_here
EMBEDDING_MODEL=text-embedding-3-small
```
