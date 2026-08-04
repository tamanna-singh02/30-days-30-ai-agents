from services.memory import update_memory

def memory_node(state):

    current_memory = state.get("memory", {})

    updated_memory = update_memory(
        current_memory,
        state["messages"]
    )

    return {
        "previous_memory": current_memory,
        "memory": updated_memory
    }

