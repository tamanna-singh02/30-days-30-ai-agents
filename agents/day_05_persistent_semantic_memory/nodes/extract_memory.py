import json

from shared.llm import get_llm
from graphs.state import AssistantState
from memory.schemas import Memory
from prompts.extraction import EXTRACTION_PROMPT


llm = get_llm()


def extract_memory(
    state: AssistantState,
):

    conversation_text = "\n".join([f"{msg.type}: {msg.content}" for msg in state["messages"]])

    response = llm.invoke(
        [
            ("system", EXTRACTION_PROMPT),
            ("user", f"Analyze this conversation and extract long-term user memories:\n\n{conversation_text}\n\nOUTPUT VALID JSON ARRAY ONLY:"),
        ]
    )

    content = response.content.strip()
    if "```" in content:
        lines = content.splitlines()
        clean_lines = []
        in_code = False
        for line in lines:
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code or not content.startswith("```"):
                clean_lines.append(line)
        content = "\n".join(clean_lines).strip()

    try:
        data = json.loads(content)
    except Exception as e:
        print(f"[Memory Extraction Error]: {e} | Content: {response.content}")
        data = []

    memories = []

    valid_categories = {"identity", "professional", "preference", "goal", "project", "experience", "skill", "custom"}

    for item in data:
        cat = item.get("category", "custom")
        if cat not in valid_categories:
            cat = "custom"
        memories.append(
            Memory(
                category=cat,
                key=item.get("key"),
                value=item["value"],
            )
        )

    return {

        "extracted_memories": memories

    }
