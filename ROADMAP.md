# 🎯 30-Day Systems-First AI Agent Curriculum

> **From Software Engineer to AI Engineer in 30 Days**  
> A hands-on, production-grade engineering roadmap focused on state machines, self-healing tool execution, memory persistence, multimodal perception, and multi-agent orchestration.

---

## 🔬 Core Architectural Principles

1. **State Machines Over Prompt Loops:** Explicit graph nodes, typed state dictionaries (`TypedDict`), and deterministic state transitions via LangGraph.
2. **Production Baseline in Every Agent:**
   - 🐳 **Dockerization:** Standalone `Dockerfile` & `docker-compose.yml` for every day.
   - 🧪 **Testing:** Unit tests written with `pytest` for state and edge cases.
   - 📊 **Observability & Cost Tracking:** Token usage, execution latency, and cost calculations (`shared/utils.py`) logged on every invocation.
   - 🛡️ **Guardrails:** Pydantic schema validation, AST safety parsing, or policy execution locks.
3. **Incremental Complexity:** Each agent introduces exactly one core architectural pattern, building on the utilities in `shared/`.

---

## 📌 Master Progression Matrix

### Week 1: Foundations, Schemas & Memory Persistence

| Status | Day | Agent Name | Core Pattern / System Focus | Tech Stack |
| :---: | :---: | :--- | :--- | :--- |
| [x] | **01** | [Structured Data Extractor](./agents/day_01_structured_output) | Schema Enforcer, Self-Healing Retries & Pydantic Guardrails | LangGraph, Pydantic, Pytest |
| [ ] | **02** | **Dynamic Prompt Synthesizer** | Meta-Prompting, Context Hydration & System Prompt Versioning | LangChain, LangGraph |
| [ ] | **03** | **Stateful Thread Assistant** | Thread Persistence, State Diffing & SQLite Checkpointers | LangGraph, SQLite |
| [ ] | **04** | **Map-Reduce Summarizer** | Context Window Budgeting & Parallel Hierarchical Chunking | Tiktoken, LangGraph |
| [ ] | **05** | **Persistent Semantic Memory** | Long-Term Key-Value Store + Vector Memory Retrieval | Redis, ChromaDB |
| [ ] | **06** | **Vector Document RAG Agent** | Chunking Trade-offs, Dense Vector Search & Citations | ChromaDB, LangChain |
| [ ] | **07** | **Hybrid Search RAG Agent** | Dense Vectors + Sparse BM25 with Relevance Re-ranking | FlashRank, BM25, ChromaDB |

---

### Week 2: External Tools, SQL & Web Automation

| Status | Day | Agent Name | Core Pattern / System Focus | Tech Stack |
| :---: | :---: | :--- | :--- | :--- |
| [ ] | **08** | **Knowledge Graph RAG Agent** | Entity Extraction, Graph Traversal & Relationship Queries | NetworkX / Neo4j |
| [ ] | **09** | **Safe SQL Query Agent** | Schema Introspection, Read-Only DB Locks & AST Guardrails | SQLAlchemy, SQLite |
| [ ] | **10** | **Tool Calling Agent** | Dynamic Tool Selection, Function Routing & Schema Binding | OpenAI Tools, Pydantic |
| [ ] | **11** | **REST API Orchestrator** | OpenAPI Spec Parsing, Endpoint Binding & Dynamic Auth | FastAPI, Requests, Pydantic |
| [ ] | **12** | **Workspace Automation Agent** | File System Traversal & Pre-flight Destructive Checklists | Python `pathlib`, Shutil |
| [ ] | **13** | **Code Inspector & AST Agent** | Abstract Syntax Trees (AST), Static Analysis & Linting | Python `ast`, Flake8 |
| [ ] | **14** | **Headless Browser Scraper** | Dynamic DOM Navigation, Scraping & Markdown Compilation | Playwright, LangGraph |

---

### Week 3: Multimodal Perception, Reasoning & Policy Rails

| Status | Day | Agent Name | Core Pattern / System Focus | Tech Stack |
| :---: | :---: | :--- | :--- | :--- |
| [ ] | **15** | **Voice Agent** | Speech-to-Text, Streaming Agent State & Audio Delivery | Whisper, ElevenLabs / gTTS |
| [ ] | **16** | **Vision RAG Agent** | Multimodal Layout Parsing (Charts, Diagrams & PDFs) | Vision LLM, PyMuPDF |
| [ ] | **17** | **Chart & Data Visualizer** | Visual Code Generation, Execution & Matplotlib Rendering | Matplotlib, Pandas, Vision LLM |
| [ ] | **18** | **Code Sandbox Agent** | Subprocess Execution, Timeouts & Exception Refinement Loops | Python `subprocess` |
| [ ] | **19** | **Plan & Execute Reasoning Agent** | Explicit Task Decomposition, Dynamic Re-planning & Task Graphs | LangGraph Custom State |
| [ ] | **20** | **Reflection Loop Agent** | Generator vs. Critic Node Iterative Refinement | LangGraph Conditional Edges |
| [ ] | **21** | **Policy Engine & Guardrails** | Sentiment Scoring, Prompt Injection Defenses & Policy Routing | Guardrails AI, Slack SDK |

---

### Week 4: Multi-Agent Systems & Enterprise Scaling

| Status | Day | Agent Name | Core Pattern / System Focus | Tech Stack |
| :---: | :---: | :--- | :--- | :--- |
| [ ] | **22** | **Multi-Agent Research Team** | Subgraph Delegation (Planner $\to$ Researcher $\to$ Writer) | LangGraph Subgraphs |
| [ ] | **23** | **Supervisor Router Agent** | Centralized Dispatcher Routing to Domain Experts | LangGraph Supervisor |
| [ ] | **24** | **Hierarchical Software Team** | Multi-Tier Subteams (PM $\to$ Lead Dev $\to$ QA Tester) | LangGraph Subgraphs |
| [ ] | **25** | **GitHub Automated PR Bot** | Webhooks, Git Diff Parsing & Inline Review Comments | PyGithub, GitHub Actions |
| [ ] | **26** | **AI Workflow Automation Agent** | Enterprise Pipeline (Email $\to$ Slack $\to$ Notion $\to$ Approval Gate) | LangGraph HITL, FastAPI |
| [ ] | **27** | **Real-Time Streaming API** | Token-by-Token Streaming & WebSocket Event Logging | FastAPI, WebSockets / SSE |
| [ ] | **28** | **Observability & RAGAS Suite** | Faithfulness, Answer Relevancy & Latency/Cost Benchmarking | RAGAS, LangSmith |
| [ ] | **29** | **Containerized Production Agent** | Multi-Container Cluster, Health Endpoints & Rate Limiting | Docker Compose, Redis, FastAPI |
| [ ] | **30** | **Autonomous AI Developer** | Capstone: Spec $\to$ Architecture $\to$ Code $\to$ Test $\to$ PR | Multi-Agent Framework |

---

## 🛠️ Daily Standard Operating Procedure (SOP)

When completing each day, execute the following 5 steps:

1. **Implement Logic:** Place code in `agents/day_XX_<name>/agent.py` using shared models from `shared/`.
2. **Add Tests:** Write unit/integration tests under `agents/day_XX_<name>/tests/test_agent.py`.
3. **Containerize:** Provide a functional `Dockerfile` and `docker-compose.yml` in the daily agent directory.
4. **Document:** Complete the 15-section `README.md` inside the agent folder.
5. **Update Roadmap:** Check the box `[x]` on this `ROADMAP.md` and hyper-link the completed project subfolder.