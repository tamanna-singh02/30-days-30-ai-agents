"""
State definitions for the Map-Reduce Summarizer.
"""
from typing import TypedDict


class SummarizerState(TypedDict, total=False):
    """
    Shared state passed between LangGraph nodes.
    """

    file_path: str
    document: str
    token_count: int
    chunk_count: int
    chunks: list[str]
    chunk_summaries: list[str]
    final_summary: str
    execution_time: float
    avg_tokens_per_chunk: float
    largest_chunk: int
    smallest_chunk: int