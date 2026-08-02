from langgraph.graph import END, StateGraph

from agents.day_01_structured_output.state import ExtractorState
from agents.day_01_structured_output.nodes import (
    extract_node,
    validate_node,
    route_validation,
)

def build_graph():
    """
    Builds and compiles the LangGraph StateGraph workflow for Day 01 agent.
    """
    graph = StateGraph(ExtractorState)

    graph.add_node("extract", extract_node)
    graph.add_node("validate", validate_node)
    graph.set_entry_point("extract")

    graph.add_edge("extract", "validate")
    graph.add_conditional_edges(
        "validate",
        route_validation,
        {
            "retry": "extract",
            "success": END,
            "failure": END,
        },
    )

    return graph.compile()
