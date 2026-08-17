# Day 09 — Tool Calling Agent

A production-grade, self-healing **Tool Calling AI Agent** featuring dynamic tool registry, Pydantic schema validation, permission checks, risk-based guardrails, parallel tool execution, and an aesthetic CLI interface powered by `rich`.

---

## 🏗️ Architecture

```text
                        User Question
                             │
                             ▼
               ┌──────────────────────────┐
               │    generate_definitions  │ ◄── ToolRegistry (Schemas)
               └─────────────┬────────────┘
                             │ (Function Specs)
                             ▼
               ┌──────────────────────────┐
               │     LLM Model Call       │ ◄── OpenAI / Groq API
               └─────────────┬────────────┘
                             │
               ┌─────────────┴─────────────┐
        (Final Answer)             (Tool Calls Returned)
               │                           │
               ▼                           ▼
        Display Output         ┌───────────────────────┐
                               │ validate_tool_call    │ ◄── Guardrails & Risk
                               └───────────┬───────────┘
                                           │
                                           ▼
                               ┌───────────────────────┐
                               │ execute_parallel      │ ◄── ThreadPoolExecutor
                               └───────────┬───────────┘
                                           │
                                           ▼
                                Returned Tool Outputs ───┐
                                                         │
                               (Loop to LLM) ────────────┘
```

---

## ✨ Features

- ✅ **Dynamic Tool Registry**: Centralized registry (`ToolRegistry`) supporting dynamic registration, categorization, and execution of tools.
- ✅ **Pydantic Schema Enforcement**: Automatic generation of OpenAI/Function-compliant JSON schemas with strict validation.
- ✅ **Parallel Tool Execution**: Multi-threaded tool execution (`ThreadPoolExecutor`) for concurrent external tool requests.
- ✅ **Security Guardrails & Risk Levels**:
  - Risk-level thresholds (`low`, `medium`, `high`) and approval checks.
  - Role-based permissions (`basic`, `developer`).
  - Allowed host filters for HTTP requests (`http_get`).
  - Safe math evaluation (`simpleeval`).
---

## 📁 Project Structure

```text
day_09_tool_calling_agent/
├── main.py                    # Interactive Rich Terminal Entrypoint
├── requirements.txt           # Agent-specific Dependencies
├── README.md                  # Documentation
└── app/
    ├── __init__.py            # Package Initializer
    ├── agent.py               # Main Agent Loop & LLM Tool Binding
    ├── discovery.py           # Tool Discovery & Filtering
    ├── executor.py            # Parallel ThreadPool Tool Executor
    ├── guardrails.py          # Tool Validation & Safety Controls
    ├── logger.py              # Logging Configuration
    ├── permissions.py         # Role-based User Permissions
    ├── policy.py              # Risk Policy Engine
    ├── registry.py            # Registered Tool Instances
    ├── router.py              # Tool Routing & Execution Wrapper
    ├── schemas.py             # Pydantic Tool Input Argument Schemas
    ├── tool.py                # Dataclass Definition for Tools
    ├── tool_registry.py       # Core ToolRegistry Class
    ├── tool_schema.py         # OpenAI JSON Schema Converter
    └── tools/
        ├── __init__.py        # Tools Package Initializer
        ├── calculator.py      # Math Calculation Tool
        ├── http.py            # Filtered HTTP GET Request Tool
        ├── string_tools.py    # String Utility Tools (Word Counter)
        └── weather.py         # Weather API Integration Tool
```

---

## 🛠️ Integrated Tools

1. **`calculate`**: Safely evaluates mathematical expressions using `simpleeval`.
2. **`get_weather`**: Fetches live weather conditions via the `wttr.in` API.
3. **`http_get`**: Performs HTTP GET requests restricted to an allowed whitelist of hosts (`jsonplaceholder.typicode.com`, `api.github.com`).
4. **`word_count`**: Counts word frequencies in input text.

---

## 🚀 Usage

Run the interactive CLI agent:

```bash
python main.py
```

Or run from the project root:

```bash
python -m agents.day_09_tool_calling_agent.main
```
