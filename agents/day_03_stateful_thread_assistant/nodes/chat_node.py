from shared.llm import get_llm
from langchain_core.messages import SystemMessage
from prompts.system_prompt import SYSTEM_PROMPT

llm=get_llm()

def chat_node(state):
    memory = state.get("memory", {})

    system_message = SystemMessage(
        content=SYSTEM_PROMPT.format(
            memory=memory
        )
    )

    response = llm.invoke(
        [system_message] + state["messages"]
    )

    return {
        "messages": [response]
    }