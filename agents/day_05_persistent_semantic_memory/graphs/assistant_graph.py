
import config

from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END

from graphs.state import AssistantState

from nodes.retrieve_memory import retrieve_memory
from nodes.assistant import assistant
from nodes.extract_memory import extract_memory
from nodes.save_memory import save_memory


builder = StateGraph(AssistantState)


builder.add_node(
    "retrieve_memory",
    retrieve_memory,
)

builder.add_node(
    "assistant",
    assistant,
)

builder.add_node(
    "extract_memory",
    extract_memory,
)

builder.add_node(
    "save_memory",
    save_memory,
)


builder.add_edge(
    START,
    "retrieve_memory",
)

builder.add_edge(
    "retrieve_memory",
    "assistant",
)

builder.add_edge(
    "assistant",
    "extract_memory",
)

builder.add_edge(
    "extract_memory",
    "save_memory",
)

builder.add_edge(
    "save_memory",
    END,
)


graph = builder.compile()