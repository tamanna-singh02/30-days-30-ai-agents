from services.diff import compute_diff


def diff_node(state):

    diff = compute_diff(
        state.get("previous_memory", {}),
        state.get("memory", {}),
    )

    return {
        "state_diff": diff
    }