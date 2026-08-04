import os
import sqlite3
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

from schemas.state import AssistantState
from nodes.chat_node import chat_node
from nodes.memory_node import memory_node
from nodes.diff_node import diff_node
from nodes.version_node import version_node

builder = StateGraph(AssistantState)

builder.add_node("chat", chat_node)
builder.add_node("memory", memory_node)
builder.add_node("diff", diff_node)
builder.add_node("version", version_node)

builder.add_edge(START, "chat")
builder.add_edge("chat", "memory")
builder.add_edge("memory", "diff")
builder.add_edge("diff", "version")
builder.add_edge("version", END)

os.makedirs("database", exist_ok=True)
conn = sqlite3.connect("database/assistant.db", check_same_thread=False)
memory = SqliteSaver(conn)

graph = builder.compile(
    checkpointer=memory
)