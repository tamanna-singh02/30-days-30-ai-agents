from datetime import datetime


def version_node(state):

    versions = list(
        state.get(
            "memory_versions",
            []
        )
    )

    versions.append(
        {
            "version": len(versions) + 1,
            "timestamp": datetime.utcnow().isoformat(),
            "memory": state["memory"],
            "diff": state["state_diff"],
        }
    )

    return {
        "memory_versions": versions
    }