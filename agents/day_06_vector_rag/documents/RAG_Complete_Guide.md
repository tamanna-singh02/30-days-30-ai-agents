# Understanding RAG (Retrieval-Augmented Generation)
### A Complete Guide — From Zero Knowledge to Advanced Concepts

---

## Table of Contents
1. The Big Picture — What RAG Is and Why It Exists
2. The Core Idea, In One Sentence
3. Anatomy of a Basic ("Naive") RAG System
4. A Full Worked Example, Step by Step
5. Chunking — Deep Dive
6. Embeddings — Deep Dive
7. Vector Databases — Deep Dive
8. Beyond Naive RAG — Advanced Techniques
9. Hybrid RAG
10. Knowledge RAG / Graph RAG
11. Vectorless RAG
12. Agentic RAG
13. Multimodal RAG
14. Comparison Table — Which RAG Type When?
15. Evaluating RAG Systems — RAGAS
16. Common Failure Modes & Challenges
17. Real-World Use Cases
18. Tools & Frameworks
19. Glossary
20. One-Page Cheat Sheet

---

## 1. The Big Picture — What RAG Is and Why It Exists

Imagine you're taking an exam. There are two kinds of exams:

- **A closed-book exam**: you can only answer using what you memorized beforehand. If you forgot something, or the syllabus changed after you studied, you're stuck — or worse, you guess confidently and get it wrong.
- **An open-book exam**: you're allowed to look things up in a textbook while answering. You still need to *understand* and *write* the answer yourself, but you're not relying purely on memory.

A large language model (LLM) like GPT, Claude, or Llama is normally sitting a **closed-book exam** for every question you ask it. It generates answers purely from patterns it learned during training. This creates three real problems:

1. **Knowledge cutoff** — the model doesn't know about anything that happened after its training data was collected.
2. **No access to private/internal data** — it has never seen your company's internal wiki, your personal notes, or last week's support tickets.
3. **Hallucination** — when the model doesn't actually know something, it doesn't necessarily say "I don't know." It can generate a fluent, confident-sounding answer that is simply wrong.

**Retrieval-Augmented Generation (RAG)** turns the closed-book exam into an open-book exam. Before the model answers, a separate system **retrieves** relevant information from an external knowledge source (documents, databases, the web, internal files) and **hands that information to the model as part of the prompt**. The model then generates its answer *grounded in* that retrieved material, instead of purely from memory.

That's it. That is the entire idea. Everything else in this document is detail on how to do that well.

---

## 2. The Core Idea, In One Sentence

> **Before answering, go look something up — then answer using what you found, and say where it came from.**

RAG = **R**etrieval (go find relevant information) + **A**ugmentation (insert that information into the prompt) + **G**eneration (let the LLM write the final answer using it).

---

## 3. Anatomy of a Basic ("Naive") RAG System

A standard RAG pipeline has two distinct phases: one that happens **once, offline** (indexing), and one that happens **every single time a user asks a question** (retrieval + generation).

### Phase A: Indexing (done ahead of time, offline)

This is the "preparing the library" phase.

1. **Collect documents** — PDFs, web pages, Word docs, Slack messages, database rows, support tickets — whatever your knowledge source is.
2. **Chunk the documents** — Break large documents into smaller pieces (a paragraph, a few sentences, a section). This matters a lot — covered in depth in Section 5.
3. **Embed each chunk** — Convert each chunk of text into a list of numbers called a **vector** (or "embedding"), which mathematically represents the *meaning* of that chunk. Covered in Section 6.
4. **Store the vectors** — Save these vectors (along with the original text) into a specialized database called a **vector database**, built for fast similarity search. Covered in Section 7.

At the end of this phase, you have a searchable "meaning index" of your entire knowledge base.

### Phase B: Retrieval + Generation (happens live, per user query)

This is the "answering the question" phase.

1. **User asks a question** — e.g., "What's our refund policy for international orders?"
2. **Embed the question** — Convert the user's question into a vector using the *same* embedding model used during indexing.
3. **Similarity search** — Compare the question's vector against every chunk's vector in the database, and pull out the **top-k** most similar chunks (commonly the top 3–10).
4. **Augment the prompt** — Build a new prompt that includes: a system instruction, the retrieved chunks (as "context"), and the original question.
5. **Generate the answer** — Send this augmented prompt to the LLM. The LLM reads the retrieved context and writes an answer grounded in it, often citing which chunk the information came from.

```
   USER QUESTION
        │
        ▼
  [Embed the question]
        │
        ▼
  [Search vector database] ──► retrieves top-k relevant chunks
        │
        ▼
  [Build augmented prompt]
   "Answer using ONLY this context: <chunks> ... Question: <question>"
        │
        ▼
  [LLM generates answer]
        │
        ▼
   FINAL ANSWER (grounded, ideally with citations)
```

---

## 4. A Full Worked Example, Step by Step

Let's say you're building a RAG chatbot for a company's internal HR policies.

**Indexing phase:**
- You have a 40-page HR handbook PDF.
- It gets split into ~120 chunks of about 200 words each.
- Each chunk is embedded into a 1536-dimension vector (a list of 1536 numbers).
- All 120 vectors + their original text are stored in a vector database like Pinecone or Chroma.

**Live phase — an employee asks:** *"How many weeks of paid parental leave do I get?"*

1. The question gets embedded into its own vector.
2. The system searches the 120 stored vectors and finds the 4 chunks whose *meaning* is closest to the question — likely the chunks about "Parental Leave," "Paid Time Off," and maybe "Eligibility Requirements," even if those chunks never use the exact words "how many weeks."
3. The prompt sent to the LLM looks something like:

```
System: You are an HR assistant. Answer only using the provided context.
If the answer isn't in the context, say you don't know.

Context:
[Chunk 1] "Employees who have completed 12 months of continuous
service are eligible for 16 weeks of paid parental leave..."
[Chunk 2] "Parental leave may be taken continuously or split into
two blocks within the first 12 months after birth or adoption..."
[Chunk 3] ...
[Chunk 4] ...

Question: How many weeks of paid parental leave do I get?
```

4. The LLM reads this and answers: *"Employees with 12+ months of continuous service are eligible for 16 weeks of paid parental leave, which can be taken continuously or split into two blocks within the first year."*

Notice: the LLM never "knew" this fact beforehand. It read it, just like you would flip to the right page in a handbook.

### Implementation Example (Minimal Naive RAG in Python)

This is a stripped-down but complete sketch — enough to see every moving part from Section 3 in actual code:

```python
import openai
import numpy as np
import faiss

# --- 1. Indexing phase (run once) ---
documents = [
    "Employees with 12+ months of continuous service are eligible for 16 weeks of paid parental leave.",
    "Parental leave can be taken continuously or split into two blocks within the first year.",
    "Sick leave accrues at 1 day per month worked, up to 12 days per year.",
    # ... hundreds more chunks in a real system
]

def embed(texts):
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return np.array([e.embedding for e in response.data], dtype="float32")

doc_vectors = embed(documents)
faiss.normalize_L2(doc_vectors)

index = faiss.IndexFlatIP(doc_vectors.shape[1])  # inner product ≈ cosine on normalized vectors
index.add(doc_vectors)

# --- 2. Retrieval phase (run per query) ---
def retrieve(query, k=3):
    query_vector = embed([query])
    faiss.normalize_L2(query_vector)
    scores, ids = index.search(query_vector, k)
    return [documents[i] for i in ids[0]]

# --- 3. Augmentation + Generation phase ---
def answer(query):
    context_chunks = retrieve(query)
    context = "\n".join(f"- {c}" for c in context_chunks)
    prompt = f"""Answer using ONLY this context. If the answer isn't
here, say you don't know.

Context:
{context}

Question: {query}"""

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

print(answer("How many weeks of paid parental leave do I get?"))
```

Swap `faiss.IndexFlatIP` for a hosted vector database (Pinecone, Chroma, Qdrant) and this same shape of code is what powers most production naive-RAG systems.

---

## 5. Chunking — Deep Dive

Chunking decides *what unit of text* gets embedded and retrieved. Get this wrong and everything downstream suffers — retrieve too little context and the answer is incomplete; retrieve too much irrelevant text and the LLM gets confused or "distracted."

**Why size matters:**
- **Too small** (e.g., one sentence): loses surrounding context; a sentence like "It must be submitted within 30 days" is meaningless without knowing *what* "it" refers to.
- **Too large** (e.g., a whole 10-page document): dilutes relevance — the vector represents an average of many different ideas, so the search becomes fuzzy, and you flood the LLM's context window with mostly irrelevant text.

**Common chunking strategies:**

| Strategy | How it works | Best for |
|---|---|---|
| **Fixed-size** | Split every N tokens/characters, e.g. every 500 tokens | Quick prototypes, simple text |
| **Fixed-size with overlap** | Same as above, but each chunk overlaps ~10-20% with the previous one | Prevents cutting a sentence/idea in half |
| **Recursive character splitting** | Tries to split on paragraph breaks first, then sentences, then words — a "graceful" fallback | General-purpose default (used by LangChain, LlamaIndex) |
| **Semantic chunking** | Uses embeddings to detect where the *topic* actually shifts, and splits there | Long, meandering documents (research papers, transcripts) |
| **Structure-aware chunking** | Splits along a document's natural structure (Markdown headers, HTML tags, code function boundaries) | Technical docs, code, structured content |

A common sweet spot in practice: **300–800 tokens per chunk with ~10-15% overlap**, adjusted per use case.

---

## 6. Embeddings — Deep Dive

An **embedding** is a way of turning text into a list of numbers (a **vector**) such that texts with *similar meaning* end up as vectors that are mathematically *close together* in space.

**Simple mental model:** imagine a map where every possible sentence gets a location. "I love dogs" and "I adore puppies" would land near each other on this map, even though they share almost no exact words. "The stock market fell today" would land far away. That "map" — with hundreds or thousands of dimensions instead of just 2 — is the embedding space.

**How similarity is measured:**
- **Cosine similarity** — measures the angle between two vectors (most common choice; ignores vector length, focuses purely on direction/meaning).
- **Dot product** — similar but also factors in magnitude.
- **Euclidean distance** — straight-line distance between two points.

**Popular embedding models (as of recent years):**
- OpenAI's `text-embedding-3-small` / `text-embedding-3-large`
- Cohere `embed-v3`
- Open-source: `sentence-transformers` (e.g., `all-MiniLM-L6-v2`), BGE, E5, Nomic Embed
- Voyage AI embeddings (popular for retrieval-focused use cases)

Note: **the same embedding model must be used for both indexing and querying** — you can't embed your documents with one model and your questions with a different one; the vector spaces won't line up.

---

## 7. Vector Databases — Deep Dive

A vector database is a database purpose-built to store millions (or billions) of vectors and answer the question: *"which stored vectors are closest to this new vector?"* — fast.

Doing this by brute force (compare the query to every single stored vector) works fine for a few thousand items but becomes too slow at scale. So vector databases use approximate nearest-neighbor (ANN) indexing algorithms:

- **HNSW (Hierarchical Navigable Small World)** — builds a multi-layer graph structure for fast approximate search; the most widely used approach today.
- **IVF (Inverted File Index)** — clusters vectors into buckets first, then searches only the most relevant buckets.
- **Product Quantization** — compresses vectors to save memory at some accuracy cost.

**Popular vector databases / libraries:**

| Tool | Notes |
|---|---|
| **FAISS** | Facebook's open-source library; not a full database, but the algorithmic backbone many tools use |
| **Chroma** | Lightweight, popular for prototyping and local apps |
| **Pinecone** | Fully managed, cloud-hosted, easy to scale |
| **Weaviate** | Open-source, supports hybrid search out of the box |
| **Qdrant** | Open-source, fast, good filtering support |
| **Milvus** | Built for very large-scale production deployments |
| **pgvector** | A Postgres extension — lets you add vector search to a database you already run |

---

## 8. Beyond Naive RAG — Advanced Techniques

The pipeline in Section 3 is the simplest version. In practice, teams add layers to fix its weaknesses.

- **Query rewriting / query expansion** — the LLM rewrites a vague user question into a clearer, more search-friendly query before retrieval happens.
- **Multi-query retrieval** — generate several variations of the user's question, retrieve for each, then merge/deduplicate the results (catches relevant chunks that a single phrasing might miss).
- **HyDE (Hypothetical Document Embeddings)** — instead of embedding the user's question directly, the LLM first writes a *hypothetical answer*, and that hypothetical answer gets embedded and used for search. This works because a hypothetical answer often resembles the real document more closely than the question does.
- **Re-ranking** — retrieve a larger initial set (e.g., top 25) using fast vector search, then use a slower but more accurate model (a "cross-encoder," e.g., Cohere Rerank) to re-score and keep only the true top 5. This two-stage "retrieve wide, then narrow" approach is one of the highest-leverage upgrades to a basic RAG system.
- **Contextual compression** — after retrieval, strip out irrelevant sentences from each chunk before sending it to the LLM, so the context is denser and cheaper.
- **Metadata filtering / self-querying** — attach metadata to chunks (date, author, department, document type) so retrieval can be filtered, e.g., "only search HR documents from 2025 onward."
- **Iterative/recursive retrieval** — the model retrieves, reads, decides it needs more information, and retrieves again — looping until it has enough to answer (useful for multi-part questions).

---

## 9. Hybrid RAG

**The problem:** Pure vector (semantic) search is great at understanding *meaning* but can be weak at exact matches — product codes, error codes, names, acronyms, IDs. A vector search for "error E402" might not rank a chunk containing exactly "E402" very highly if the surrounding wording differs.

**The fix — Hybrid RAG** combines two retrieval methods:

1. **Sparse/keyword retrieval** (e.g., **BM25**, a classic algorithm from traditional search engines) — matches exact words and terms, great at precision for specific terms.
2. **Dense/vector retrieval** — matches meaning, great at synonyms, paraphrasing, and conceptual similarity.

Both retrieval methods run on the same query, and their results are merged — commonly using a technique called **Reciprocal Rank Fusion (RRF)**, which combines rankings from multiple retrieval methods into a single fair ranking without needing to compare raw scores directly (since BM25 scores and cosine similarity scores aren't on the same scale).

**When to use it:** Almost always a solid default for real-world systems — especially where users search for specific terms (legal codes, product SKUs, medical codes, technical documentation) *as well as* natural-language questions. Weaviate, Elasticsearch, and Qdrant all support hybrid search natively.

---

## 10. Knowledge RAG / Graph RAG

**The problem:** Plain vector search treats each chunk as an isolated island. It's bad at answering questions that require connecting facts *across* multiple documents — e.g., "Which suppliers used by Company A are also used by its main competitor, Company B?" That answer might require piecing together relationships buried across a dozen unrelated documents. Vector similarity alone won't reliably assemble that chain of connections.

**The fix — Knowledge Graph RAG (often called "GraphRAG")** builds a structured **knowledge graph** — a network of **entities** (people, companies, products, concepts) connected by **relationships** (works-for, supplies, causes, located-in) — from the source documents, and uses that graph *in addition to or instead of* pure vector search.

**How it's typically built:**
1. Run entity extraction and relationship extraction over the documents (often using an LLM) to identify: "Entity A → relationship → Entity B."
2. Store this as a graph, often in a graph database like **Neo4j**, or as a structured knowledge graph.
3. Some approaches (like Microsoft's GraphRAG) also detect **communities** — clusters of tightly related entities — and generate summaries of each community ahead of time, so broad "big picture" questions can be answered from pre-computed summaries instead of stitching together raw chunks live.

**How it's queried:**
- Graph traversal (follow relationship edges) or graph query languages like **Cypher**.
- Often combined with vector search: use vectors to find a relevant *starting entity*, then traverse the graph from there.

**Benefits:**
- Handles **multi-hop reasoning** ("who reports to the person who approved this budget?") far better than vector search alone.
- Better at holistic/summarization questions across an entire corpus.
- More explainable — you can literally show the path of relationships that led to an answer.

**Trade-offs:**
- Significantly more complex and expensive to build and maintain than a vector index.
- Requires good entity/relationship extraction, which can be noisy on messy real-world data.
- Best suited for domains that are genuinely relationship-rich (org charts, supply chains, scientific literature, legal case law, fraud investigation).

---

## 11. Vectorless RAG

**The problem it addresses:** Vector databases add infrastructure complexity, embedding costs, and can struggle with exact-match/structured queries. Sometimes teams want the *spirit* of RAG (look things up before answering) without embeddings and vector databases at all.

**"Vectorless RAG"** refers to retrieval approaches that skip vector embeddings entirely. Common flavors:

- **Keyword/full-text search only** — using something like Elasticsearch or PostgreSQL full-text search (BM25-style ranking) with no embeddings involved at all. Simple, fast, and excellent for exact terms, but weaker on paraphrased or conceptual queries.
- **LLM-based/agentic retrieval** — instead of a similarity search, the LLM itself is given tools (like a file browser, a search function, or a database query tool) and decides what to look up and where, step by step, the way a human researcher would open folders and skim documents. This trades a fixed pipeline for a flexible, reasoning-driven one.
- **Text-to-SQL / structured retrieval** — for RAG over structured business data (a sales database, an inventory system), the "retrieval" step is the LLM writing a SQL query to pull exactly the rows it needs, rather than searching unstructured text.
- **Long-context "stuffing"** — with today's very large context windows (some models can accept hundreds of thousands of tokens), some systems skip retrieval altogether for smaller corpora and just feed the *entire* knowledge base into the prompt every time. This isn't retrieval in the traditional sense, but it accomplishes the same underlying goal (grounding the model in real information) without a vector store.

**Why choose vectorless approaches:**
- Simpler infrastructure — one less specialized system to run and maintain.
- Often better for exact-match-heavy domains (legal citations, product codes, structured records).
- Can be cheaper at smaller scale (no embedding generation/storage costs).

**Trade-offs:**
- Loses the "understands meaning, not just words" superpower of embeddings.
- Full-context stuffing gets expensive and slower as the knowledge base grows, and very long contexts can suffer from the "lost in the middle" problem (see Section 16).
- LLM-driven agentic retrieval can be slower and less predictable than a fixed pipeline.

---

## 12. Agentic RAG

Worth calling out separately: **Agentic RAG** wraps the entire retrieval process in an LLM-driven agent loop. Instead of a fixed "retrieve once, generate once" pipeline, the model can:

- Decide *whether* retrieval is even needed for a given question.
- Choose *which* knowledge source to search (vector DB, web search, SQL database, an API).
- Retrieve, evaluate whether the results are good enough, and retrieve again with a refined query if not.
- Combine information from multiple sources before answering.

This is the architecture behind most modern "AI research assistant" style products — it's more flexible and often more accurate, at the cost of more latency and more LLM calls.

---

## 13. Multimodal RAG

Retrieval doesn't have to be text-only. **Multimodal RAG** retrieves and reasons over images, tables, charts, audio transcripts, and video frames alongside text — for example, retrieving the correct diagram from a technical manual, or the correct chart from a financial report, using models that can embed and compare images and text in the same vector space (e.g., CLIP-style embeddings).

---

## 14. Comparison Table — Which RAG Type When?

| Type | Core mechanism | Great at | Watch out for |
|---|---|---|---|
| **Naive RAG** | Single vector search + generate | Simple Q&A over a document set | Poor on exact terms, multi-hop questions |
| **Advanced RAG** | Naive RAG + re-ranking, query rewriting, HyDE | Higher accuracy, still fairly simple to run | More moving parts, more latency |
| **Hybrid RAG** | Vector search + keyword (BM25) search, merged | Mixed natural-language + exact-term queries | Needs a fusion strategy (e.g., RRF) |
| **Knowledge/Graph RAG** | Knowledge graph traversal (+ optional vectors) | Multi-hop reasoning, relationship-heavy domains | Expensive to build/maintain, complex |
| **Vectorless RAG** | Keyword search, agentic tool use, SQL, or context-stuffing | Exact-match data, structured data, simpler infra | Weaker semantic/paraphrase understanding |
| **Agentic RAG** | LLM decides when/how/where to retrieve, iteratively | Complex, multi-step, multi-source questions | Slower, less predictable, more costly |
| **Multimodal RAG** | Retrieval across text, images, tables | Manuals, reports, mixed-media knowledge bases | Needs multimodal embedding models |

---

## 15. Evaluating RAG Systems — RAGAS

Once you've built a RAG system, how do you know if it's actually *good*? This is trickier than evaluating a normal ML model because a RAG system has **two separate components that can each fail independently**:

1. The **retriever** can fail (pulls back irrelevant or incomplete chunks).
2. The **generator** can fail (has good chunks, but still hallucinates or answers poorly).

**RAGAS** ("RAG Assessment") is an open-source evaluation framework built specifically to measure both halves of this pipeline, without needing a human to manually grade every answer. It typically uses a strong LLM as an automated "judge" to score outputs against a defined set of metrics.

**Core RAGAS metrics:**

| Metric | What it measures | Plain-English question it answers |
|---|---|---|
| **Faithfulness** | Whether the generated answer's claims are actually supported by the retrieved context | "Did the model make anything up that isn't in what it retrieved?" |
| **Answer Relevancy** | Whether the generated answer actually addresses the question asked | "Did it answer the actual question, or wander off-topic?" |
| **Context Precision** | Whether the retrieved chunks that *are* relevant are ranked near the top | "Out of what was retrieved, was the useful stuff surfaced first?" |
| **Context Recall** | Whether the retrieval step pulled back *all* the information needed to answer correctly (compared against a ground-truth answer) | "Did we retrieve everything necessary, or miss something important?" |
| **Context Entity Recall** | Whether key entities (names, dates, terms) from the ground truth appear in retrieved context | "Did we retrieve the specific facts/entities that matter?" |
| **Answer Correctness / Answer Similarity** | How factually close the final answer is to a known correct answer | "Is the final answer actually right?" |

**Why this matters:** a system can have *perfect* retrieval but a generator that hallucinates anyway (low faithfulness), or a generator that's very careful and faithful but a retriever that keeps missing the right documents (low context recall). RAGAS scores let you diagnose *which half* of the pipeline needs fixing instead of just knowing "the answers are sometimes bad."

**Other RAG evaluation tools worth knowing:**
- **TruLens** — tracing and evaluation, focused on feedback functions similar to RAGAS's metrics.
- **DeepEval** — a broader LLM evaluation framework with RAG-specific metrics.
- **Arize Phoenix** — observability and evaluation, strong on tracing retrieval pipelines visually.
- **LangSmith** — evaluation and tracing tooling from the LangChain team.

---

## 16. Common Failure Modes & Challenges

- **Garbage in, garbage out** — bad chunking or messy source documents (broken tables, scanned PDFs with OCR errors) poison everything downstream.
- **"Lost in the middle"** — LLMs tend to pay more attention to information at the very start and very end of a long context, and can under-weight facts buried in the middle. Stuffing too much retrieved text into the prompt can actually *hurt* accuracy.
- **Irrelevant retrieval** — if the retriever pulls the wrong chunks, even a perfect generator will produce a wrong or unhelpfully generic answer.
- **Hallucination despite grounding** — the model can still ignore the retrieved context and answer from its own memory, especially if the retrieved context is ambiguous or contradicts what it "believes."
- **Stale index** — the vector database is a snapshot; if the source documents change and the index isn't refreshed, the system confidently serves outdated information.
- **Cost & latency** — embedding, retrieval, re-ranking, and generation all add up; more advanced pipelines (agentic, multi-hop) can be noticeably slower and pricier per query.
- **Chunk boundary problems** — an important fact split awkwardly across two chunks may never be fully retrieved together.

---

## 17. Real-World Use Cases

- **Customer support chatbots** — answering from product docs, help-center articles, and past ticket resolutions.
- **Enterprise/internal knowledge search** — "ask your company's wiki/Slack/Confluence a question" tools.
- **Legal & compliance** — retrieving relevant clauses, case law, or regulations before drafting or reviewing documents.
- **Healthcare & medical Q&A** — grounding answers in clinical guidelines or research literature (with heavy guardrails, given the stakes).
- **Coding assistants** — retrieving relevant code, documentation, or past commits from a codebase before answering a coding question.
- **Financial research** — retrieving from earnings reports, filings, and market data to support analyst queries.

---

## 18. Tools & Frameworks

| Category | Examples |
|---|---|
| **Orchestration frameworks** | LangChain, LlamaIndex, Haystack, Semantic Kernel |
| **Vector databases** | Pinecone, Weaviate, Qdrant, Chroma, Milvus, pgvector |
| **Graph databases (for GraphRAG)** | Neo4j, Amazon Neptune |
| **Keyword/full-text search** | Elasticsearch, OpenSearch, Postgres full-text search |
| **Re-ranking models** | Cohere Rerank, BGE-reranker, cross-encoder models |
| **Evaluation** | RAGAS, TruLens, DeepEval, Arize Phoenix, LangSmith |

---

## 19. Glossary

- **Embedding** — a numerical vector representation of text that captures meaning.
- **Vector database** — a database optimized to store and search embeddings by similarity.
- **Chunking** — splitting large documents into smaller retrievable pieces.
- **Top-k retrieval** — pulling back the k most similar chunks to a query.
- **Cosine similarity** — a common way to measure how close two vectors are in meaning.
- **Re-ranking** — a second, more precise scoring pass over an initial set of retrieved results.
- **Hallucination** — when an LLM generates confident but false or unsupported information.
- **BM25** — a classic keyword-based ranking algorithm used in traditional search engines.
- **RRF (Reciprocal Rank Fusion)** — a method for merging rankings from multiple retrieval methods.
- **Knowledge graph** — a network of entities connected by labeled relationships.
- **Grounding** — making an LLM's answer based on retrieved, verifiable source material rather than pure memory.
- **RAGAS** — an evaluation framework specifically built to score RAG pipelines on faithfulness, relevancy, and retrieval quality.

---

## 20. One-Page Cheat Sheet

- **RAG = look things up, then answer** — it turns a closed-book LLM into an open-book one.
- **Indexing (offline):** collect docs → chunk → embed → store in a vector DB.
- **Query time:** embed question → retrieve top-k similar chunks → build augmented prompt → LLM generates grounded answer.
- **Chunking and embedding quality make or break the whole system** — garbage chunks in, garbage answers out.
- **Hybrid RAG** = vector search + keyword search, for the best of both semantic and exact-match retrieval.
- **Knowledge/Graph RAG** = use an entity-relationship graph for multi-hop, relationship-heavy questions.
- **Vectorless RAG** = skip embeddings entirely — use keyword search, agentic tool use, SQL, or long-context stuffing instead.
- **Agentic RAG** = let the LLM decide when, where, and how many times to retrieve.
- **RAGAS** evaluates both halves of the system separately: is the *retrieval* good (precision/recall of context), and is the *generation* good (faithfulness/relevancy of the answer)?
- Watch for: bad chunking, lost-in-the-middle, stale indexes, and hallucination even when grounded.

---

*This guide is meant as a living reference — you can hand it to someone with zero background and they should be able to follow it start to finish, or use it as your own refresher before designing a RAG system.*

---

## 21. System Configuration & Technical API Reference

To support production system administration, error troubleshooting, and service integration, the following exact environment configuration parameters, security credentials, error codes, and REST API routes are maintained:

### Key Environment Variables & Connection Specs
- **Redis Cache Connection URL**: `REDIS_URL=redis://:secret_pass@cache.internal.domain:6379/0` — Specifies the full Redis cluster connection string used for query result caching, rate limiting, and session state persistence.
- **JWT Signing Secret**: `JWT_SECRET=super_secret_jwt_token_key_2026_prod` — The cryptographic secret key required for signing and verifying JSON Web Tokens for user authentication.
- **Database Connection Pool**: `DATABASE_POOL_SIZE=20` — Controls the maximum number of active database connections in the primary PostgreSQL connection pool.

### HTTP Status Codes & Troubleshooting
- **401 Unauthorized**: Returned by the API gateway when a request lacks a valid Bearer token, when `JWT_SECRET` verification fails, or when authentication credentials have expired.
- **403 Forbidden**: Indicates the caller is authenticated but lacks required role-based permissions to access the requested resource.

### Core API Endpoints
- **Token Generation Endpoint**: `POST /api/v1/auth/token` — Exchanges client API credentials for an authenticated short-lived JWT access token.
- **Vector Search Endpoint**: `POST /api/v1/retrieval/search` — Accepts user query strings and vector parameters to return top-k matching document chunks.

