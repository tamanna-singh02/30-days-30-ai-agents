import sys
from pathlib import Path
from typing import TypedDict

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from config import settings
from prompts.answer_prompt import get_rag_prompt
from retrieval.reranker import Reranker
from retrieval.retriever import Retriever



class RAGState(TypedDict, total=False):
    question: str
    retrieved_documents: list
    reranked_documents: list
    context: str
    answer: str
    sources: list
    retrieval_count: int
    reranked_count: int


class RAGGraph:
    """
    LangGraph-based RAG agent.
    """

    def __init__(self):

        self.retriever = Retriever()

        self.reranker = Reranker()

        try:
            self.llm = ChatOpenAI(
                model=settings.OPENAI_MODEL,
                temperature=0,
                api_key=settings.OPENAI_API_KEY,
            )
        except Exception:
            from shared.llm import get_llm
            self.llm = get_llm("groq", model="llama-3.3-70b-versatile", temperature=0)

        self.prompt = get_rag_prompt()

        self.graph = self._build_graph()

    def _retrieve(self, state: RAGState):
        """
        Retrieve relevant documents.
        """

        question = state["question"]

        documents = self.retriever.retrieve(
            query=question,
            k=settings.RETRIEVAL_K,
        )

        return {
            "retrieved_documents": documents,
            "retrieval_count": len(documents),
        }

    def _rerank(self, state: RAGState):
        """
        Rerank retrieved documents.
        """

        question = state["question"]

        retrieved_documents = state.get(
            "retrieved_documents",
            [],
        )

        reranked = self.reranker.rerank(
            query=question,
            documents=retrieved_documents,
            top_k=settings.TOP_K,
        )

        return {
            "reranked_documents": reranked,
            "reranked_count": len(reranked),
        }

    def _build_context(
        self,
        state: RAGState,
    ):
        """
        Convert retrieved documents into
        LLM-readable context.
        """

        documents = state.get(
            "reranked_documents",
            [],
        )

        context_parts = []
        sources = []

        for item in documents:

            document = item.document

            page = document.metadata.get(
                "page",
                "unknown",
            )

            source = document.metadata.get(
                "source",
                "unknown",
            )

            # PDF page numbers are usually zero-indexed.
            display_page = (
                page + 1
                if isinstance(page, int)
                else page
            )

            context_parts.append(
                f"""
Source: {source}
Page: {display_page}

{document.page_content}
"""
            )

            sources.append(
                {
                    "source": source,
                    "page": display_page,
                    "score": item.score,
                }
            )

        return {
            "context": "\n\n".join(context_parts),
            "sources": sources,
        }


    def _check_context(
        self, state: RAGState,
    ):
        documents = state.get(
            "reranked_documents",
            [],
        )

        if not documents:
            return {
                "answer": (
                    "I couldn't find enough relevant "
                    "information in the provided document "
                    "to answer this question."
                )
            }
        
        return {}

    def _should_generate(self, state: RAGState):
        documents = state.get(
            "reranked_documents",
            [],
        )
        if not documents:
            return "no_context"
        return "generate_answer"
    

    def _generate_answer(
        self,
        state: RAGState,
    ):
        """
        Generate a grounded answer.
        """

        question = state["question"]
        context = state.get(
            "context",
            "",
        )

        messages = self.prompt.invoke(
            {
                "question": question,
                "context": context,
            }
        )

        try:
            response = self.llm.invoke(messages)
            answer_text = response.content
        except Exception as e:
            if "quota" in str(e).lower() or "429" in str(e) or "credit" in str(e).lower():
                from shared.llm import get_llm
                fallback_llm = get_llm("groq", model="llama-3.3-70b-versatile", temperature=0)
                response = fallback_llm.invoke(messages)
                answer_text = response.content
            else:
                raise e

        return {
            "answer": answer_text
        }

    def _build_graph(self):

        workflow = StateGraph(RAGState)

        workflow.add_node(
            "retrieve",
            self._retrieve,
        )

        workflow.add_node(
            "rerank",
            self._rerank,
        )

        workflow.add_node(
            "build_context",
            self._build_context,
        )

        workflow.add_node(
            "generate_answer",
            self._generate_answer,
        )

        workflow.add_node(
            "no_context",
            self._check_context,
        )

        workflow.add_edge(
            START,
            "retrieve",
        )

        workflow.add_edge(
            "retrieve",
            "rerank",
        )

        workflow.add_edge(
            "rerank",
            "build_context",
        )

        workflow.add_conditional_edges(
            "build_context",
             self._should_generate,
             {
                "no_context": "no_context",
                "generate_answer": "generate_answer",
             }
        )

        workflow.add_edge(
            "generate_answer",
            END,
        )

        return workflow.compile()

    def invoke(
        self,
        question: str,
    ) -> RAGState:

        return self.graph.invoke(
            {
                "question": question
            }
        )