# Day 03: Stateful Thread Assistant 💾

A stateful, memory-aware conversational assistant built with **LangGraph**, **Pydantic**, and **SQLite**. It persists thread-specific conversation state, automatically extracts structured user memory across turns, tracks state diffs, and logs immutable memory version history.

---

## 📌 Architecture & Workflow

```text
[START] ──> (chat) ──> (memory) ──> (diff) ──> (version) ──> [END]
```

1. **`chat`**: Combines user messages with stored long-term memory to generate context-aware LLM responses.
2. **`memory`**: Uses structured LLM extraction (`UserMemory`) to automatically capture user metadata (name, hobbies, preferences, company, city, professional role).
3. **`diff`**: Computes field-level state changes (`compute_diff`) between current memory and newly extracted updates.
4. **`version`**: Records an immutable snapshot of memory state, diffs, and timestamps per version.

---

## ✨ Features

- **SQLite Thread Checkpointing**: Persistent conversation threads stored in `database/assistant.db` using `SqliteSaver`.
- **Structured User Memory**: Pydantic-enforced memory schema capturing names, preferences, hobbies, and work details.
- **State Diffing & Version Control**: Real-time tracking of memory updates and complete version history logs per thread.
- **Rich Terminal UI**: Elegant CLI interface built with `rich` panels, tables, and clean status indicators.

---

## 🚀 How to Run

Run the assistant CLI from the project root:

```bash
python agents/day_03_stateful_thread_assistant/app.py
```

Or using the virtual environment directly:

```powershell
.\venv\Scripts\python.exe agents/day_03_stateful_thread_assistant/app.py
```

### Interactive Usage Example
1. Enter a **Thread ID** (e.g. `thread_1` or `user_session_123`).
2. Chat naturally with the assistant (e.g., *"Hi, my name is Tamanna and I prefer Python."*).
3. Re-run using the **same Thread ID** to verify persistent thread memory.
4. Type `exit` to close the session.

---

## 🧪 Tests

Execute unit and edge-case test suites:

```bash
pytest agents/day_03_stateful_thread_assistant/tests/
```
