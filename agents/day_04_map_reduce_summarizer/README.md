# Day 4: Map-Reduce Document Summarizer (V2)

A production-grade, state-driven document summarization agent built using **LangGraph**, **LangChain**, and **tiktoken**. It splits large documents into token-aware chunks, summarizes each chunk in parallel/sequence (Map phase), and synthesizes them into a single, high-quality, coherent summary (Reduce phase).

---

## 🏗️ Architecture

```
Document
   ↓
Chunking (Token-Aware)
   ↓
  Map (Summarize Chunks)
   ↓
 Reduce (Combine Summaries)
   ↓
Final Summary
```

---

## ✨ Features

- ✅ **Token counting**: Accurately counts tokens using `tiktoken` to respect LLM context limits.
- ✅ **Token-aware chunking**: Splits documents dynamically with configurable chunk size and overlap.
- ✅ **Map-Reduce summarization**: Scalable workflow to summarize documents of any size.
- ✅ **LangGraph workflow**: Pure state-driven graph execution.
- ✅ **Execution logging & tracker**: Visual progress tracking and node execution timing.
- ✅ **Summary artifact saving**: Automatically persists results to `output/summary.md`.
- ✅ **CLI file argument support**: Summarize any file passed via command line argument (`python app.py path/to/file.txt`).
- ✅ **Token statistics**: Detailed analysis including average tokens per chunk, largest chunk, and smallest chunk.
- ✅ **PDF & Text support**: Automatic text extraction from `.pdf` and `.txt` files.
- ✅ **Cost-efficient document processing**: Minimized token waste using targeted production prompts.

---

## 📁 Project Structure

```
day_04_map_reduce_summarizer/
├── app.py           # CLI Entrypoint & Console Formatting
├── config.py        # Settings (Chunk sizes, default file, output path)
├── graph.py         # LangGraph workflow definition
├── nodes.py         # State nodes (load, chunk, map, reduce)
├── prompts.py       # Production map and reduce prompt templates
├── state.py         # SummarizerState TypedDict definition
├── utils.py         # Document loader (PDF/TXT), tiktoken chunking & stats
├── data/
│   ├── sample_report.txt
│   └── sample_article.txt
└── README.md
```

---

## 🚀 Usage

### 1. Default Run (Sample Report)

```bash
python -m agents.day_04_map_reduce_summarizer.app
```

### 2. Custom File Input

Summarize any text or PDF file:

```bash
python -m agents.day_04_map_reduce_summarizer.app agents/day_04_map_reduce_summarizer/data/sample_article.txt
```

---

## 📊 Sample Output

```
==================================================
Loading document...
==================================================
✓ Document loaded successfully

==================================================
Counting tokens...
==================================================
Total Tokens : 1,248

==================================================
Splitting document...
==================================================
Created 2 chunks

==================================================
Summarizing chunks...
==================================================
Summarizing chunk 1/2...
Summarizing chunk 2/2...

==================================================
MAP-REDUCE SUMMARIZER
==================================================

Document:
agents/day_04_map_reduce_summarizer/data/sample_article.txt

Total Tokens:
1,248

Chunks:
2

Average Tokens Per Chunk:
624.0

Largest Chunk:
710

Smallest Chunk:
538

Execution Time:
3.45 sec

--------------------------------------------
FINAL SUMMARY
--------------------------------------------
...

==================================================
✓ Summary saved to output/summary.md
==================================================
```
