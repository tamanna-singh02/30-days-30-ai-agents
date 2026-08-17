from concurrent.futures import ThreadPoolExecutor

from app.router import execute_tool


MAX_WORKERS = 5


def execute_tools_parallel(tool_calls):

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        futures = {
            executor.submit(
                execute_tool,
                call.function.name if hasattr(call, "function") else getattr(call, "name", ""),
                call.function.arguments if hasattr(call, "function") else getattr(call, "arguments", "{}"),
            ): call
            for call in tool_calls
        }

        outputs = []

        for future, call in futures.items():

            result = future.result()
            call_id = getattr(call, "id", getattr(call, "call_id", ""))

            outputs.append({
                "role": "tool",
                "tool_call_id": call_id,
                "content": str(result),
            })

    return outputs