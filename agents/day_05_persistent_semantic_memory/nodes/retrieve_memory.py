
from langchain_core.documents import Document
from graphs.state import AssistantState
from memory.memory_manager import memory_manager


def retrieve_memory(
    state: AssistantState,
):
    last_message = state["messages"][-1]
    query = last_message.content

    # 1. Retrieve vector similarity matches
    vector_memories = memory_manager.retrieve(
        query=query,
        k=5,
    )

    # 2. Retrieve structured KV store facts
    kv_facts = memory_manager.list_all_facts()
    kv_docs = []
    for fact in kv_facts:
        fact_content = f"{fact.key}: {fact.value}" if fact.key else fact.value
        kv_docs.append(
            Document(
                page_content=fact_content,
                metadata={"category": fact.category, "key": fact.key or ""}
            )
        )

    # 3. Merge & deduplicate by page_content
    seen = set()
    combined_memories = []
    for doc in kv_docs + vector_memories:
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            combined_memories.append(doc)

    return {
        "retrieved_memories": combined_memories
    }