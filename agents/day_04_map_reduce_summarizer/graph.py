"""
LangGraph workflow for Map-Reduce Summarizer.
"""

from langgraph.graph import StateGraph, START, END

from agents.day_04_map_reduce_summarizer.state import SummarizerState
from agents.day_04_map_reduce_summarizer.nodes import (
    load_document_node,
    chunk_document_node,
    map_summarize_node,
    reduce_summaries_node,
)

builder = StateGraph(SummarizerState)

# Add nodes
builder.add_node("load_document", load_document_node)
builder.add_node("chunk_document", chunk_document_node)
builder.add_node("map_summarize", map_summarize_node)
builder.add_node("reduce_summaries", reduce_summaries_node)

# Add edges
builder.add_edge(START, "load_document")
builder.add_edge("load_document", "chunk_document")
builder.add_edge("chunk_document", "map_summarize")
builder.add_edge("map_summarize", "reduce_summaries")
builder.add_edge("reduce_summaries", END)

graph = builder.compile()