from typing import List, TypedDict

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage

from memory.schemas import Memory


class AssistantState(TypedDict):
    """
    Shared state across the LangGraph workflow.
    """

    # Chat history
    messages: List[BaseMessage]

    # Memories retrieved from Chroma
    retrieved_memories: List[Document]

    # Memories extracted from current conversation
    extracted_memories: List[Memory]

    # Final assistant response
    response: str
