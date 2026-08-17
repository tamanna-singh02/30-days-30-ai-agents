import os

from dotenv import load_dotenv
from openai import OpenAI

from app.router import execute_tool
from app.tool_schema import generate_tool_definitions
from app.executor import execute_tools_parallel


load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

if groq_key:
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=groq_key,
    )
    DEFAULT_MODEL = os.getenv("MODEL_NAME", "openai/gpt-oss-120b")
else:
    client = OpenAI(
        api_key=openai_key
    )
    DEFAULT_MODEL = "gpt-4o-mini"

MAX_TOOL_ITERATIONS = 10


def run_agent(user_input: str):

    tools = generate_tool_definitions()

    messages = [
        {"role": "user", "content": user_input}
    ]

    for _ in range(MAX_TOOL_ITERATIONS):

        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            tools=tools,
        )

        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            return message.content or ""

        tool_outputs = execute_tools_parallel(
            message.tool_calls
        )

        messages.extend(tool_outputs)

    return "Agent stopped: maximum tool iterations reached."