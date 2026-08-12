from typing import TypedDict

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from config import settings
from prompts.answer_prompt import get_rag_prompt
from retrieval.hybrid_pipeline import HybridSearchPipeline


class HybridRAGState(TypedDict, total=False):
    query: str
    question: str
    retrieved_documents: list[Document]
    reranked_documents: list
    retrieval_scores: list[float]
    context: str
    answer: str
    sources: list[dict]
    retrieval_method: str


class HybridRAGGraph:
    """
    LangGraph-based Hybrid Search RAG Agent.
    Pipeline:
      1. Retrieve (Dense + BM25 -> RRF -> CrossEncoder Reranker)
      2. Build Context
      3. Generate Answer (using LLM with prompt & grounded context)
    """

    def __init__(self):
        self.pipeline = HybridSearchPipeline()

        try:
            self.llm = ChatOpenAI(
                model=settings.OPENAI_MODEL,
                temperature=0,
                api_key=settings.OPENAI_API_KEY,
            )
        except Exception:
            from shared.llm import get_llm

            self.llm = get_llm(
                "groq", model="llama-3.3-70b-versatile", temperature=0
            )

        self.prompt = get_rag_prompt()
        self.graph = self._build_graph()

    def _retrieve(self, state: HybridRAGState) -> dict:
        query = state.get("query") or state.get("question", "")

        results = self.pipeline.retrieve(
            query=query,
            candidate_k=settings.RETRIEVAL_K,
            final_k=settings.TOP_K,
        )

        documents = [res.document for res in results]
        scores = [res.score for res in results]

        return {
            "retrieved_documents": documents,
            "reranked_documents": results,
            "retrieval_scores": scores,
            "retrieval_method": "Dense + BM25 + RRF + Cross-Encoder",
        }

    def _build_context(self, state: HybridRAGState) -> dict:
        reranked = state.get("reranked_documents", [])

        context_parts = []
        sources = []

        for item in reranked:
            doc = item.document
            score = item.score
            page = doc.metadata.get("page", "unknown")
            source = doc.metadata.get("source", "unknown")

            display_page = page + 1 if isinstance(page, int) else page

            context_parts.append(
                f"Source: {source} (Page {display_page})\nScore: {score:.4f}\n\n{doc.page_content}"
            )

            sources.append(
                {
                    "source": source,
                    "page": display_page,
                    "score": score,
                    "chunk_id": doc.metadata.get("chunk_id", ""),
                }
            )

        return {
            "context": "\n\n---\n\n".join(context_parts),
            "sources": sources,
        }

    def _check_context(self, state: HybridRAGState) -> dict:
        reranked = state.get("reranked_documents", [])
        if not reranked:
            return {
                "answer": "I couldn't find relevant information in the document context to answer your query."
            }
        return {}

    def _should_generate(self, state: HybridRAGState) -> str:
        reranked = state.get("reranked_documents", [])
        if not reranked:
            return "no_context"
        return "generate_answer"

    def _generate_answer(self, state: HybridRAGState) -> dict:
        query = state.get("query") or state.get("question", "")
        context = state.get("context", "")

        messages = self.prompt.invoke(
            {
                "question": query,
                "context": context,
            }
        )

        try:
            response = self.llm.invoke(messages)
            answer_text = response.content
        except Exception as e:
            if any(
                term in str(e).lower()
                for term in ["quota", "429", "credit", "api_key", "unauthorized"]
            ):
                from shared.llm import get_llm

                fallback_llm = get_llm(
                    "groq", model="llama-3.3-70b-versatile", temperature=0
                )
                response = fallback_llm.invoke(messages)
                answer_text = response.content
            else:
                raise e

        return {"answer": answer_text}

    def _build_graph(self):
        workflow = StateGraph(HybridRAGState)

        workflow.add_node("retrieve", self._retrieve)
        workflow.add_node("build_context", self._build_context)
        workflow.add_node("generate_answer", self._generate_answer)
        workflow.add_node("no_context", self._check_context)

        workflow.add_edge(START, "retrieve")
        workflow.add_edge("retrieve", "build_context")

        workflow.add_conditional_edges(
            "build_context",
            self._should_generate,
            {
                "no_context": "no_context",
                "generate_answer": "generate_answer",
            },
        )

        workflow.add_edge("generate_answer", END)
        workflow.add_edge("no_context", END)

        return workflow.compile()

    def invoke(self, query: str) -> HybridRAGState:
        return self.graph.invoke({"query": query, "question": query})