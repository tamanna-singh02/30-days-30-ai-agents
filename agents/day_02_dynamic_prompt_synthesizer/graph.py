"""
Langgraph workflow
"""

from langgraph.graph import (
    END, START, StateGraph,
)

from agents.day_02_dynamic_prompt_synthesizer.nodes import(
    analyze_request,
    build_dynamic_prompt,
    generate_response,
)

from agents.day_02_dynamic_prompt_synthesizer.state import AgentState

builder = StateGraph(AgentState)

builder.add_node("analyze_request", analyze_request)
builder.add_node("build_prompt",build_dynamic_prompt)
builder.add_node("generate_response",generate_response)

builder.add_edge(START, "analyze_request")
builder.add_edge("analyze_request","build_prompt")
builder.add_edge("build_prompt", "generate_response")
builder.add_edge("generate_response",END)

graph = builder.compile()
