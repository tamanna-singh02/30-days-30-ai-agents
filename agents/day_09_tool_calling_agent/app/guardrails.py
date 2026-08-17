from app.registry import registry


class ToolGuardrailError(Exception):
    pass


def validate_tool_call(
    tool_name: str,
    arguments: dict,
):
    """
    Validate whether a tool call is allowed.
    """

    # 1. Tool exists
    if not registry.exists(tool_name):
        raise ToolGuardrailError(
            f"Unknown tool: {tool_name}"
        )

    tool = registry.get(tool_name)

    # 2. Tool enabled
    if not tool.enabled:
        raise ToolGuardrailError(
            f"Tool '{tool_name}' is disabled."
        )

    # 3. Schema validation
    schema = tool.schema

    try:
        validated = schema.model_validate(arguments)
    except Exception as e:
        raise ToolGuardrailError(
            f"Invalid arguments: {str(e)}"
        )

    # 4. Approval check
    if tool.requires_approval:
        raise ToolGuardrailError(
            f"Tool '{tool_name}' requires approval."
        )

    return validated