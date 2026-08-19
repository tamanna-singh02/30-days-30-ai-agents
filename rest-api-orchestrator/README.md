# 🌐 Day 10: REST API Orchestrator

An autonomous AI agent that ingests OpenAPI / REST API definitions into a central registry, decomposes natural language user goals into multi-step execution DAGs using meta-prompting, resolves dynamic data dependencies between steps, and executes requests with exponential backoff retries, timeouts, and validation guardrails.

---

## 🎯 Architecture Overview

```text
                     ┌──────────────────────────┐
                     │   User Natural Language  │
                     │         Goal Input       │
                     └─────────────┬────────────┘
                                   │
                                   ▼
                     ┌──────────────────────────┐
                     │       LLM Planner        │
                     │  (Goal -> ExecutionPlan) │
                     └─────────────┬────────────┘
                                   │
                                   ▼
                     ┌──────────────────────────┐
                     │      Plan Validator      │
                     │ (Cycle & Spec Checklist) │
                     └─────────────┬────────────┘
                                   │
                                   ▼
 ┌────────────────────────────────────────────────────────────────────┐
 │                     Orchestration Engine DAG                       │
 │                                                                    │
 │  ┌──────────────────────┐              ┌────────────────────────┐  │
 │  │ Dependency Resolver  │─────────────►│   Reference Resolver   │  │
 │  │   (Ready Steps)      │              │ ({{step1.data[0].id}}) │  │
 │  └──────────────────────┘              └───────────┬────────────┘  │
 │                                                    │               │
 │                                                    ▼               │
 │  ┌──────────────────────┐              ┌────────────────────────┐  │
 │  │ Resilience Middleware│◄─────────────│     Step Executor      │  │
 │  │  (Retries & Timeouts)│              │    (HTTP Execution)    │  │
 │  └──────────────────────┘              └────────────────────────┘  │
 └────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
                     ┌──────────────────────────┐
                     │   Execution Summary State│
                     └──────────────────────────┘
```

---

## 📁 Package Structure

```text
rest-api-orchestrator/
├── app/
│   ├── main.py                  # Entrypoint CLI with Rich UI output
│   ├── planner/
│   │   ├── planner.py           # LLM Plan Synthesizer with Heuristic fallback
│   │   └── prompts.py           # System prompts for API plan generation
│   ├── orchestrator/
│   │   ├── engine.py            # Async DAG Execution Engine
│   │   ├── executor.py          # Step execution coordinator
│   │   ├── dependency.py        # Dependency graph resolver & step scheduler
│   │   ├── resolver.py          # {{step_id.field[0].id}} Template Reference Resolver
│   │   ├── validator.py         # Plan schema, API, & cycle detector
│   │   └── state.py             # ExecutionState & StepResult tracker
│   ├── api/
│   │   ├── registry.py          # Central APIRegistry & endpoint lookup
│   │   ├── client.py            # Async HTTP Client wrapper
│   │   └── schemas.py           # Endpoint definitions builder
│   ├── validation/
│   │   ├── request_validator.py # Request parameter type & required check
│   │   └── response_validator.py# Response status code & schema check
│   ├── resilience/
│   │   ├── retry.py             # Exponential backoff retry handler
│   │   └── timeout.py           # Execution timeout guard
│   └── models/
│       ├── api.py               # Pydantic model for APIDefinition & Parameter
│       ├── plan.py              # Pydantic model for ExecutionPlan & ExecutionStep
│       └── result.py            # Pydantic model for OrchestrationResult
├── tests/                       # Unit tests (Pytest)
├── requirements.txt             # Package dependencies
└── README.md                    # Architecture & Usage Documentation
```

---

## ⚡ Key Features

1. **OpenAPI / Endpoint Registry:** Standardized Pydantic schemas for registering HTTP endpoints, parameters, methods, schemas, and resilience settings.
2. **LLM Dynamic Planning:** Decomposes complex user instructions into dynamic multi-step execution graphs.
3. **Template Reference Resolution:** Resolves output variables from prior steps (`"{{get_orders.orders[0].id}}"`) automatically before executing dependent API calls.
4. **Resilience & Guardrails:** Retries transient network failures using exponential backoff, enforces execution timeouts per endpoint, and validates step DAGs against circular dependencies.
5. **Parallel Step Execution:** Executes independent graph nodes concurrently via `asyncio.gather`.

---

## 🚀 Quickstart

### 1. Installation & Environment

```bash
pip install -r requirements.txt
```

### 2. Run the Main Agent Pipeline

```bash
python -m app.main
```

### 3. Run Unit Tests

```bash
pytest
```
