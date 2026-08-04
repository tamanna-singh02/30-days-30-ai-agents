from typing import TypedDict, Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AssistantState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

    memory: dict

    previous_memory: dict

    state_diff: dict

    memory_versions: list[dict]