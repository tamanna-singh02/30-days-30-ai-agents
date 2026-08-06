from graphs.state import AssistantState
from memory.memory_manager import memory_manager


def save_memory(
    state: AssistantState,
):

    memories = state.get("extracted_memories", [])

    if memories:

        memory_manager.save_many(memories)

    return {}
