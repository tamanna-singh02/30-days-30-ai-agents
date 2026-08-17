from app.registry import registry


def generate_tool_definitions():

    definitions = []

    for tool in registry.list():

        schema = tool.schema.model_json_schema()

        definitions.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": schema,
            },
        })

    return definitions