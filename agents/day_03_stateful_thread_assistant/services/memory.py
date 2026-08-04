from langchain_core.messages import HumanMessage, AIMessage

from shared.llm import get_llm
from schemas.user_memory import UserMemory
from prompts.memory_prompt import SYSTEM_PROMPT

llm=get_llm().with_structured_output(UserMemory)

def build_chat(messages):
    conversation = []

    for message in messages:

        if isinstance(message, HumanMessage):
            role="Human"

        elif isinstance(message, AIMessage):
            role="Assistant"
        
        else:
            role="System"

        conversation.append(
            f"{role}: {message.content}"
        )
        
    return "\n".join(conversation)

def update_memory(existing_memory: dict, messages):
    conversation = build_chat(messages)

    prompt = f"""
    Existing Memory

    {existing_memory}

    Converstion
    {conversation}
    """

    memory = llm.invoke(
        [
            ("system", SYSTEM_PROMPT),
            ("human", prompt)
        ]
    )

    return memory.model_dump()