from app.tool import Tool


class ToolRegistry:

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool):

        if tool.name in self._tools:
            raise ValueError(
                f"Tool already registered: {tool.name}"
            )

        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:

        if name not in self._tools:
            raise KeyError(
                f"Unknown tool: {name}"
            )

        return self._tools[name]

    def list(self) -> list[Tool]:

        return list(self._tools.values())

    def exists(self, name: str) -> bool:

        return name in self._tools