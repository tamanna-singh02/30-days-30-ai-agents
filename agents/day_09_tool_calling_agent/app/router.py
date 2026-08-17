import json
from concurrent.futures import ThreadPoolExecutor, TimeoutError

from app.registry import registry
from app.guardrails import ToolGuardrailError


def execute_tool(
    tool_name: str,
    arguments: str,
):

    try:

        tool = registry.get(tool_name)

        parsed_arguments = json.loads(arguments)

        # Validate
        validated_arguments = (
            tool.schema.model_validate(
                parsed_arguments
            )
        )

        # Approval
        if tool.requires_approval:
            return (
                f"APPROVAL_REQUIRED: "
                f"Tool '{tool.name}' requires approval."
            )

        # Execute with timeout
        with ThreadPoolExecutor(
            max_workers=1
        ) as executor:

            future = executor.submit(
                tool.handler,
                **validated_arguments.model_dump(),
            )

            try:

                result = future.result(
                    timeout=tool.timeout
                )

            except TimeoutError:

                return (
                    f"Tool '{tool.name}' "
                    f"timed out after "
                    f"{tool.timeout}s."
                )

        return str(result)

    except KeyError as e:

        return f"Tool error: {str(e)}"

    except json.JSONDecodeError as e:

        return (
            f"Invalid JSON arguments: {str(e)}"
        )

    except Exception as e:

        return (
            f"Tool execution failed: {str(e)}"
        )

def describe_tools():

    for tool in registry.list():

        print(
            f"{tool.name}: "
            f"{tool.description} "
            f"[risk={tool.risk_level}]"
        )