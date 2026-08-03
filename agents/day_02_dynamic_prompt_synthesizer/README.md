# Day 02: Dynamic Prompt Synthesizer 🎯

An intelligent LangGraph agent that analyzes a user's intent, dynamically constructs an optimized prompt tailored to that intent, and generates a refined response.

## 📌 Architecture & Workflow

```
[START] ──> (analyze_request) ──> (build_prompt) ──> (generate_response) ──> [END]
```

1. **`analyze_request`**: Uses LLM structured output (`PromptStrategy`) to analyze intent (`email`, `summarization`, `extraction`), tone, output format, and constraints.
2. **`build_prompt`**: Dynamically synthesizes an optimal prompt template using the detected strategy parameters.
3. **`generate_response`**: Executes the synthesized prompt with the LLM to deliver the final response.

## 🚀 Usage

Run the agent from the project root:

```bash
python -m agents.day_02_dynamic_prompt_synthesizer.main
```
