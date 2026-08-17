USER_PERMISSIONS = {

    "basic": {
        "calculate",
        "get_weather",
        "word_count",
    },

    "developer": {
        "calculate",
        "get_weather",
        "word_count",
        "http_get",
    },
}


def can_use_tool(
    role: str,
    tool_name: str,
) -> bool:

    allowed_tools = USER_PERMISSIONS.get(
        role,
        set(),
    )

    return tool_name in allowed_tools