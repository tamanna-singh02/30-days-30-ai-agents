from app.registry import registry


def discover_tools(
    category: str | None = None,
):

    tools = registry.list()

    if category is None:
        return tools

    return [
        tool
        for tool in tools
        if tool.category == category
    ]