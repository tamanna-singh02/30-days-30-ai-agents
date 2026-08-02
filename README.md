# 🚀 30 AI Agents in 30 Days

<div align="center">

### Building AI Agents with Systems-First Engineering

*30 hands-on projects exploring modern AI engineering, from structured outputs and RAG to multi-agent orchestration.*

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent_Framework-purple)
![LangChain](https://img.shields.io/badge/LangChain-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

---

# 📖 Overview

Large Language Models have made building AI applications more accessible than ever. However, production AI systems require much more than prompt engineering.

This repository documents my journey of building **30 AI agents in 30 days**, with each project focusing on a different engineering concept—from structured outputs and retrieval systems to browser automation, multimodal agents, and distributed multi-agent architectures.

The objective is not only to build working AI agents, but to understand the engineering principles behind reliable, maintainable, and scalable AI systems.

---

# 🎯 Goals

- Build 30 AI agents from scratch
- Learn modern agent architectures
- Apply software engineering best practices
- Explore real-world AI system design
- Document architectural decisions and trade-offs
- Build a portfolio of practical AI engineering projects

---

# 🏗 Engineering Principles

Every project follows a consistent engineering approach:

- Clean Architecture
- Modular Design
- Separation of Concerns
- Strong Typing
- State-Driven Workflows
- Validation & Guardrails
- Unit Testing
- Dockerized Development
- Production-Oriented Documentation

---

# 🛠 Tech Stack

### AI Frameworks

- LangGraph
- LangChain

### Models

- OpenAI
- Anthropic
- Ollama

### Backend

- FastAPI
- PostgreSQL
- Redis

### Validation

- Pydantic
- Guardrails AI

### Vector Search

- ChromaDB
- pgvector

### Browser Automation

- Playwright

### Evaluation

- RAGAS
- LangSmith

### Infrastructure

- Docker
- GitHub Actions

---

# 📂 Repository Structure

```text
30-ai-agents-30-days/

│
├── .github/
│   └── workflows/
│
├── agents/
│   ├── day_01_structured_output/
│   ├── day_02_dynamic_prompt_synthesizer/
│   ├── ...
│   └── day_30_autonomous_ai_developer/
│
├── shared/
│   ├── config.py
│   ├── llm.py
│   ├── logger.py
│   ├── utils.py
│   ├── guardrails.py
│   ├── observability/
│   ├── evaluation/
│   ├── memory/
│   └── caching/
│
├── docs/
├── assets/
├── templates/
│
├── requirements.txt
├── docker-compose.yml
├── README.md
└── ROADMAP.md
```

---

# 🗺️ Roadmap

## Week 1 — Foundations

| Day | Agent | Core Pattern | Tech Stack | Difficulty | Status |
|-----|-------|--------------|------------|------------|--------|
| 1 | Structured Data Extractor | Schema Guardrails & Self-Healing Retries | LangGraph, Pydantic | 🟢 Easy | 🚧 |
| 2 | Dynamic Prompt Synthesizer | Meta-Prompting & Context Injection | LangChain, LangGraph | 🟢 Easy | ⏳ |
| 3 | Stateful Thread Assistant | Thread Persistence & State Diffing | LangGraph, SQLite | 🟢 Easy | ⏳ |
| 4 | Map-Reduce Summarizer | Context Window Budgeting & Chunking | Tiktoken, LangGraph | 🟡 Medium | ⏳ |
| 5 | Persistent Semantic Memory | Long-Term Memory + Vector Retrieval | Redis, ChromaDB | 🟡 Medium | ⏳ |
| 6 | Vector Document RAG Agent | Chunking & Dense Vector Search | ChromaDB, LangChain | 🟡 Medium | ⏳ |
| 7 | Hybrid Search RAG Agent | Dense + Sparse Retrieval | FlashRank, BM25 | 🟡 Medium | ⏳ |

---

## Week 2 — SQL & Tool Use

| Day | Agent | Core Pattern | Tech Stack | Difficulty | Status |
|-----|-------|--------------|------------|------------|--------|
| 8 | Knowledge Graph RAG Agent | Graph Traversal | NetworkX, Neo4j | 🔴 Hard | ⏳ |
| 9 | Safe SQL Query Agent | Schema Introspection | SQLAlchemy, SQLite | 🟡 Medium | ⏳ |
| 10 | Tool Calling Agent | Dynamic Tool Selection | LangGraph, Pydantic | 🟡 Medium | ⏳ |
| 11 | REST API Orchestrator | OpenAPI Parsing | FastAPI, Requests | 🟡 Medium | ⏳ |
| 12 | Workspace Automation Agent | File System Automation | pathlib, shutil | 🟢 Easy | ⏳ |
| 13 | Code Inspector & AST Agent | Static Analysis | Python AST, Flake8 | 🟡 Medium | ⏳ |
| 14 | Headless Browser Scraper | Dynamic DOM Extraction | Playwright, LangGraph | 🟡 Medium | ⏳ |

---

## Week 3 — Multimodal AI

| Day | Agent | Core Pattern | Tech Stack | Difficulty | Status |
|-----|-------|--------------|------------|------------|--------|
| 15 | Voice Agent | Speech Processing | Whisper, ElevenLabs | 🔴 Hard | ⏳ |
| 16 | Vision RAG Agent | Multimodal Parsing | Vision LLM, PyMuPDF | 🔴 Hard | ⏳ |
| 17 | Chart & Data Visualizer | Visual Code Generation | Matplotlib, Vision LLM | 🟡 Medium | ⏳ |
| 18 | Code Sandbox Agent | Reflection Loop | subprocess | 🔴 Hard | ⏳ |
| 19 | Plan & Execute Agent | Dynamic Planning | LangGraph | 🔴 Hard | ⏳ |
| 20 | Reflection Loop Agent | Generator–Critic Pattern | LangGraph | 🟡 Medium | ⏳ |
| 21 | Policy Engine & Guardrails | Prompt Injection Defense | Guardrails AI | 🔴 Hard | ⏳ |

---

## Week 4 — Multi-Agent Systems

| Day | Agent | Core Pattern | Tech Stack | Difficulty | Status |
|-----|-------|--------------|------------|------------|--------|
| 22 | Multi-Agent Research Team | Planner–Researcher–Writer | LangGraph Subgraphs | 🔴 Hard | ⏳ |
| 23 | Supervisor Router Agent | Centralized Routing | LangGraph Supervisor | 🔴 Hard | ⏳ |
| 24 | Hierarchical Software Team | Multi-Level Coordination | LangGraph Subgraphs | 🔴 Hard | ⏳ |
| 25 | GitHub Automated PR Bot | Automated Code Review | PyGithub, GitHub Actions | 🔴 Hard | ⏳ |
| 26 | AI Workflow Automation Agent | Multi-App Automation | LangGraph | 🔴 Hard | ⏳ |
| 27 | Real-Time Streaming API | Streaming Responses | FastAPI, WebSockets | 🟡 Medium | ⏳ |
| 28 | Observability & RAGAS Suite | AI Evaluation | RAGAS, LangSmith | 🔴 Hard | ⏳ |
| 29 | Containerized Production Agent | Deployment & Health Checks | Docker, Redis, FastAPI | 🟡 Medium | ⏳ |
| 30 | Autonomous AI Developer | End-to-End Multi-Agent System | Multi-Agent Architecture | 🔴 Hard | ⏳ |

---

# 📚 What You'll Learn

Throughout these projects, you'll explore topics including:

- Agentic Workflows
- LangGraph State Machines
- Retrieval-Augmented Generation (RAG)
- Long-Term Memory
- Structured Outputs
- Tool Calling
- Browser Automation
- SQL Agents
- Multimodal AI
- Reflection & Self-Correction
- Multi-Agent Systems
- AI Evaluation
- Observability
- Streaming APIs
- Production Deployment

---

# 🚀 Getting Started

```bash
git clone https://github.com/<your-username>/30-ai-agents-30-days.git

cd 30-ai-agents-30-days

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file from `.env.example` and add the required API keys.

Run the first project:

```bash
python -m agents.day_01_structured_output.agent
```

---

# 📈 Progress

- ✅ Projects Completed: **0 / 30**
- 🚧 Current Project: **Day 1 – Structured Data Extractor**
- ⭐ Final Goal: **30 AI Agents**

---

# 🤝 Connect With Me

- **LinkedIn:** *(Add your profile here)*

I'm documenting the engineering decisions, lessons learned, and implementation details as I build each project in public.

---

## ⭐ Support the Project

If you find this repository useful, consider giving it a star. It helps others discover the project and motivates me to keep building and sharing the journey.