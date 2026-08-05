"""
LangGraph nodes for the Map-Reduce Summarizer.
"""

from langchain_core.messages import HumanMessage
from shared.llm import get_llm
from shared.logger import logger
from shared.utils import ExecutionTracker

from agents.day_04_map_reduce_summarizer.prompts import (
    MAP_PROMPT,
    REDUCE_PROMPT,
)
from agents.day_04_map_reduce_summarizer.utils import (
    load_document,
    count_tokens,
    split_into_chunks,
    calculate_chunk_stats,
)
from agents.day_04_map_reduce_summarizer.state import SummarizerState
from agents.day_04_map_reduce_summarizer.config import INPUT_FILE

llm = get_llm()


def load_document_node(state: SummarizerState):
    """Load the input document with logging and execution tracking."""
    file_path = state.get("file_path") or INPUT_FILE

    logger.info("=" * 50)
    logger.info("Loading document...")
    logger.info("=" * 50)

    with ExecutionTracker("Load Document"):
        document = load_document(file_path)

    logger.info("[OK] Document loaded successfully\n")
    return {
        "file_path": file_path,
        "document": document,
    }


def chunk_document_node(state: SummarizerState):
    """Count tokens, split document into chunks, and compute statistics."""
    document = state["document"]

    logger.info("=" * 50)
    logger.info("Counting tokens...")
    logger.info("=" * 50)

    with ExecutionTracker("Count Tokens"):
        token_count = count_tokens(document)

    logger.info(f"Total Tokens : {token_count:,}\n")

    logger.info("=" * 50)
    logger.info("Splitting document...")
    logger.info("=" * 50)

    with ExecutionTracker("Chunk Document"):
        chunks = split_into_chunks(document)
        stats = calculate_chunk_stats(chunks)

    chunk_count = len(chunks)
    logger.info(f"Created {chunk_count} chunks\n")

    return {
        "token_count": token_count,
        "chunk_count": chunk_count,
        "chunks": chunks,
        "avg_tokens_per_chunk": stats["avg_tokens_per_chunk"],
        "largest_chunk": stats["largest_chunk"],
        "smallest_chunk": stats["smallest_chunk"],
    }


def map_summarize_node(state: SummarizerState):
    """Summarize each chunk with per-chunk progress logging."""
    chunks = state["chunks"]
    summaries = []
    chunk_count = len(chunks)

    logger.info("=" * 50)
    logger.info("Summarizing chunks...")
    logger.info("=" * 50)

    with ExecutionTracker("Map Summarize"):
        for index, chunk in enumerate(chunks, start=1):
            logger.info(f"Summarizing chunk {index}/{chunk_count}...")
            prompt = MAP_PROMPT.format(chunk=chunk)
            response = llm.invoke([HumanMessage(content=prompt)])
            summaries.append(response.content)

    logger.info(f"\n[OK] Completed summarization of {len(summaries)} chunks\n")
    return {
        "chunk_summaries": summaries,
    }


def reduce_summaries_node(state: SummarizerState):
    """Combine chunk summaries into a final coherent summary."""
    logger.info("=" * 50)
    logger.info("Reducing summaries...")
    logger.info("=" * 50)

    with ExecutionTracker("Reduce Summaries"):
        joined = "\n\n".join(state["chunk_summaries"])
        prompt = REDUCE_PROMPT.format(summaries=joined)
        response = llm.invoke([HumanMessage(content=prompt)])

    logger.info("[OK] Final summary generated successfully\n")
    return {
        "final_summary": response.content,
    }