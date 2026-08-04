# 🎯 30-Day Systems-First AI Agent Curriculum

> **From Software Engineer to AI Engineer in 30 Days**  
> A hands-on, production-grade engineering roadmap focused on state machines, self-healing tool execution, memory persistence, multimodal perception, and multi-agent orchestration.

---

## 🔬 Curriculum Philosophy & Progression

The 30-day curriculum is designed sequentially, with each week introducing a fundamental tier of enterprise AI system architecture:

```text
Week 1: Foundations, Schemas & Memory
 └── Typed State, Pydantic Retries, Map-Reduce & Persistent Vector Memory
      ↓
Week 2: External Tools, SQL & Web Automation
 └── Knowledge Graphs, Safe AST Execution, Dynamic Tool Binding & Headless Scrapers
      ↓
Week 3: Multimodal Perception, Reasoning & Policy Rails
 └── Voice Streaming, Vision RAG, Code Sandboxes, Reflection Loops & Policy Engines
      ↓
Week 4: Multi-Agent Systems & Enterprise Scaling
 └── Subgraph Delegation, Hierarchical Teams, Streaming APIs & Autonomous AI Developers
```

---

## 📌 Master Progression Matrix

### Week 1: Foundations, Schemas & Memory Persistence

| Status | Day | Agent Name | Core Architectural Pattern | Tech Stack |
| :---: | :---: | :--- | :--- | :--- |
| [x] | **01** | [Structured Data Extractor](./agents/day_01_structured_output) | Schema Enforcer, Self-Healing Retries & Pydantic Guardrails | LangGraph, Pydantic, Pytest |
| [x] | **02** | [Dynamic Prompt Synthesizer](./agents/day_02_dynamic_prompt_synthesizer) | Meta-Prompting, Context Hydration & System Prompt Versioning | LangChain, LangGraph, Jinja2 |
| [x] | **03** | [Stateful Thread Assistant](./agents/day_03_stateful_thread_assistant) | Thread Persistence, State Diffing & SQLite Checkpointers | LangGraph, SQLite, Pydantic |
| [ ] | **04** | **Map-Reduce Summarizer** | Context Window Budgeting & Parallel Hierarchical Chunking | Tiktoken, LangGraph, Asyncio |
| [ ] | **05** | **Persistent Semantic Memory** | Long-Term Key-Value Store + Vector Memory Retrieval | Redis, ChromaDB, LangChain |
| [ ] | **06** | **Vector Document RAG Agent** | Chunking Trade-offs, Dense Vector Search & Citations | ChromaDB, LangChain, PyPDF |
| [ ] | **07** | **Hybrid Search RAG Agent** | Dense Vectors + Sparse BM25 with Relevance Re-ranking | FlashRank, BM25, ChromaDB |

---

### Week 2: External Tools, SQL & Web Automation

| Status | Day | Agent Name | Core Architectural Pattern | Tech Stack |
| :---: | :---: | :--- | :--- | :--- |
| [ ] | **08** | **Knowledge Graph RAG Agent** | Entity Extraction, Graph Traversal & Relationship Queries | NetworkX / Neo4j, LangChain |
| [ ] | **09** | **Safe SQL Query Agent** | Schema Introspection, Read-Only DB Locks & AST Guardrails | SQLAlchemy, SQLite, Pydantic |
| [ ] | **10** | **Tool Calling Agent** | Dynamic Tool Selection, Function Routing & Schema Binding | OpenAI Tools, Pydantic, Requests |
| [ ] | **11** | **REST API Orchestrator** | OpenAPI Spec Parsing, Endpoint Binding & Dynamic Auth | FastAPI, Requests, Pydantic |
| [ ] | **12** | **Workspace Automation Agent** | File System Traversal & Pre-flight Destructive Checklists | Python `pathlib`, Shutil, Pytest |
| [ ] | **13** | **Code Inspector & AST Agent** | Abstract Syntax Trees (AST), Static Analysis & Linting | Python `ast`, Flake8, Black |
| [ ] | **14** | **Headless Browser Scraper** | Dynamic DOM Navigation, Scraping & Markdown Compilation | Playwright, LangGraph, BeautifulSoup4 |

---

### Week 3: Multimodal Perception, Reasoning & Policy Rails

| Status | Day | Agent Name | Core Architectural Pattern | Tech Stack |
| :---: | :---: | :--- | :--- | :--- |
| [ ] | **15** | **Voice Agent** | Speech-to-Text, Streaming Agent State & Audio Delivery | Whisper, ElevenLabs / gTTS, PyAudio |
| [ ] | **16** | **Vision RAG Agent** | Multimodal Layout Parsing (Charts, Diagrams & PDFs) | Vision LLM, PyMuPDF, OpenCV |
| [ ] | **17** | **Chart & Data Visualizer** | Visual Code Generation, Execution & Matplotlib Rendering | Matplotlib, Pandas, Vision LLM |
| [ ] | **18** | **Code Sandbox Agent** | Subprocess Execution, Timeouts & Exception Refinement Loops | Python `subprocess`, Resource Limits |
| [ ] | **19** | **Plan & Execute Reasoning Agent** | Explicit Task Decomposition, Dynamic Re-planning & Task Graphs | LangGraph Custom State |
| [ ] | **20** | **Reflection Loop Agent** | Generator vs. Critic Node Iterative Refinement | LangGraph Conditional Edges |
| [ ] | **21** | **Policy Engine & Guardrails** | Sentiment Scoring, Prompt Injection Defenses & Policy Routing | Guardrails AI, Slack SDK, Pydantic |

---

### Week 4: Multi-Agent Systems & Enterprise Scaling

| Status | Day | Agent Name | Core Architectural Pattern | Tech Stack |
| :---: | :---: | :--- | :--- | :--- |
| [ ] | **22** | **Multi-Agent Research Team** | Subgraph Delegation (Planner $\to$ Researcher $\to$ Writer) | LangGraph Subgraphs, Tavily |
| [ ] | **23** | **Supervisor Router Agent** | Centralized Dispatcher Routing to Domain Experts | LangGraph Supervisor |
| [ ] | **24** | **Hierarchical Software Team** | Multi-Tier Subteams (PM $\to$ Lead Dev $\to$ QA Tester) | LangGraph Subgraphs, Pytest |
| [ ] | **25** | **GitHub Automated PR Bot** | Webhooks, Git Diff Parsing & Inline Review Comments | PyGithub, GitHub Actions |
| [ ] | **26** | **AI Workflow Automation Agent** | Enterprise Pipeline (Email $\to$ Slack $\to$ Approval Gate) | LangGraph HITL, FastAPI |
| [ ] | **27** | **Real-Time Streaming API** | Token-by-Token Streaming & WebSocket Event Logging | FastAPI, WebSockets / SSE |
| [ ] | **28** | **Observability & RAGAS Suite** | Faithfulness, Answer Relevancy & Latency/Cost Benchmarking | RAGAS, LangSmith |
| [ ] | **29** | **Containerized Production Agent** | Multi-Container Cluster, Health Endpoints & Rate Limiting | Docker Compose, Redis, FastAPI |
| [ ] | **30** | **Autonomous AI Developer** | Capstone: Spec $\to$ Architecture $\to$ Code $\to$ Test $\to$ PR | Multi-Agent Framework |

---

## 🛠️ Daily Standard Operating Procedure (SOP)

When completing each daily agent challenge, follow this standardized 5-step development lifecycle:

1. **Architecture & State Design:** Define the agent `TypedDict` state (`state.py`), schemas (`schemas.py`), nodes (`nodes.py`), and graph transitions (`graph.py`) inside `agents/day_XX_<name>/`.
2. **Dependency Injection:** Bind services (`services.py`) via the shared LLM factory (`shared/llm.py`) to support multi-provider execution.
3. **Unit Testing:** Implement unit and edge-case tests in `agents/day_XX_<name>/tests/test_agent.py` using `pytest`.
4. **Containerization & Documentation:** Provide a standalone `Dockerfile` and write a daily `README.md` explaining the agent's graph topology and execution instructions.
5. **Roadmap & Progress Sync:** Mark the checkbox `[x]` on this `ROADMAP.md` matrix and hyperlink the completed agent directory.

---

## 🛡️ Production Quality Gates

Every completed daily build must satisfy the following verification criteria before being merged:

- ✅ **Zero Hardcoded LLM Instances:** Uses `shared/llm.py:get_llm()`.
- ✅ **Type Safety:** Passes `pyright` static type validation.
- ✅ **Automated Test Coverage:** `pytest` passes cleanly.
- ✅ **No Secret Leaks:** All API keys loaded exclusively via environment variables.
- ✅ **Self-Healing Verification:** Handles malformed outputs or retries gracefully.