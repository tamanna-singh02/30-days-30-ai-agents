"""LangGraph workflow definition for Safe SQL Agent."""

from langgraph.graph import StateGraph, END
from agents.day_08_safe_sql_agent.agent.state import SQLAgentState
from agents.day_08_safe_sql_agent.agent.nodes import (
    introspect_schema_node,
    generate_sql_node,
    validate_sql_node,
    execute_sql_node,
    route_after_validation,
)


def build_graph():
    workflow = StateGraph(SQLAgentState)

    workflow.add_node("introspect_schema", introspect_schema_node)
    workflow.add_node("generate_sql", generate_sql_node)
    workflow.add_node("validate_sql", validate_sql_node)
    workflow.add_node("execute_sql", execute_sql_node)

    workflow.set_entry_point("introspect_schema")
    workflow.add_edge("introspect_schema", "generate_sql")
    workflow.add_edge("generate_sql", "validate_sql")

    workflow.add_conditional_edges(
        "validate_sql",
        route_after_validation,
        {
            "execute": "execute_sql",
            "retry": "generate_sql",
            "fail": END,
        },
    )

    workflow.add_edge("execute_sql", END)

    return workflow.compile()


graph = build_graph()
