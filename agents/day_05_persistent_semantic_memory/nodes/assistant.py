from langchain_core.messages import AIMessage
from shared.llm import get_llm

from graphs.state import AssistantState
from prompts.assistant import ASSISTANT_PROMPT


llm = get_llm()


def assistant(
    state: AssistantState,
):

    memories = "\n".join(

        memory.page_content

        for memory in state["retrieved_memories"]

    )

    prompt = ASSISTANT_PROMPT.format(

        memories=memories

    )

    response = llm.invoke(

        [

            ("system", prompt),

            *state["messages"],

        ]

    )

    return {

        "messages": [

            AIMessage(content=response.content)

        ],

        "response": response.content,

    }
