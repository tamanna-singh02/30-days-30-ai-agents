# Day 08 — Safe SQL Agent

A security-first text-to-SQL AI agent built using **LangGraph**, **SQLGlot AST validation guardrails**, schema introspection, read-only locks, and automatic self-healing retry loops.

---

## 🏗️ Architecture

```text
                       User Question
                            │
                            ▼
              ┌──────────────────────────┐
              │    introspect_schema     │ ◄── PostgreSQL / Demo DB
              └─────────────┬────────────┘
                            │ (Formatted Schema)
                            ▼
              ┌──────────────────────────┐
              │       generate_sql       │ ◄── LLM SQL Generator
              └─────────────┬────────────┘
                            │ (Candidate SQL)
                            ▼
              ┌──────────────────────────┐
              │       validate_sql       │ ── AST Security Guardrails
              └─────────────┬────────────┘
                            │
              ┌─────────────┴─────────────┐
        (Allowed)                   (Forbidden / Syntax Error)
              │                           │
              ▼                           ▼
  ┌───────────────────────┐   ┌───────────────────────┐
  │      execute_sql      │   │  Self-Healing Retry   │
  └──────────┬────────────┘   │   (Max 3 Iterations)  │
             │                └───────────┬───────────┘
             ▼                            │
      Query Results ──────────────────────┘
```

---

## ✨ Features

- ✅ **AST Guardrail Validation (SQLGlot)**: Inspects the Abstract Syntax Tree before query execution.
  - Enforces `SELECT`-only queries (blocks `DELETE`, `DROP`, `UPDATE`, `INSERT`, `ALTER`, etc.).
  - Enforces mandatory `LIMIT` clauses ($\le 1000$).
  - Blocks access to forbidden system schemas (`pg_catalog`, `information_schema`).
  - Blocks dangerous system functions (`PG_READ_FILE`, `PG_WRITE_FILE`, `PG_LS_DIR`, `DBLINK`).
  - Validates tables, columns, and column aliases against introspected schema.
- ✅ **Dynamic Schema Introspection**: Extracts table definitions, data types, and foreign key relationships.
- ✅ **Self-Healing Retry Loop**: Feeds AST validation errors back to the generator to correct malformed queries automatically.
- ✅ **Resilient Demo DB Fallback**: Automatically provides an in-memory database with sample datasets if a live PostgreSQL database is offline.
- ✅ **Rich 2-Color UI**: Minimalist terminal output powered by `rich` (`cyan` and `white`) without box borders.

---

## 📁 Project Structure

```text
day_08_safe_sql_agent/
├── main.py                    # Driver & Main Execution Entrypoint
├── config.py                  # Database DSN & Environment Settings
├── requirements.txt           # Agent-specific Dependencies
├── README.md                  # Project Documentation
├── ui.py                      # Rich 2-Color Terminal Interface
├── agent/
│   ├── graph.py               # LangGraph Workflow Compilation
│   ├── nodes.py               # Node Handlers & Router Logic
│   └── state.py               # SQLAgentState TypedDict
├── database/
│   ├── connection.py          # PostgreSQL Connection & In-Memory Fallback
│   └── schema.py              # Schema Introspection & Formatting
├── guardrails/
│   ├── ast_validator.py       # SQLGlot AST Validation Engine
│   └── policies.py            # Security Policies & Limits
├── sql/
│   ├── generator.py           # LLM SQL Generator (with retry feedback)
│   └── parser.py              # SQLGlot Parser Helper
└── tests/
    ├── test_ast_validator.py   # AST Guardrail Unit Tests
    ├── test_graph.py          # State Graph & Routing Tests
    └── test_schema.py         # Schema Introspection Tests
```

---

## 🚀 Usage

### Run Agent Workflow

```bash
python -m agents.day_08_safe_sql_agent.main
```

### Run Pytest Suite

```bash
pytest agents/day_08_safe_sql_agent/tests/
```
