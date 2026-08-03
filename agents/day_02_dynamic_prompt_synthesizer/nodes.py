"""
Node definitions for dynamic prompt synthesizer.
"""

from langchain_core.messages import HumanMessage

from shared import ExecutionTracker, get_llm, logger
from agents.day_02_dynamic_prompt_synthesizer.prompt_builder import (
    build_prompt
)
from agents.day_02_dynamic_prompt_synthesizer.prompts import (
    STRATEGY_PROMPT,
    SYSTEM_PROMPT
)
from agents.day_02_dynamic_prompt_synthesizer.schemas import (
    PromptStrategy
)
from agents.day_02_dynamic_prompt_synthesizer.state import AgentState
from agents.day_02_dynamic_prompt_synthesizer.utils import validate_prompt

llm = get_llm()


# Node 1 - Analyze Request
def analyze_request(state: AgentState) -> AgentState:
    """
    Determine the best prompt strategy.
    """
    with ExecutionTracker("Analyze Request"):
        logger.info("Analyzing user request...")

        structured_llm = llm.with_structured_output(PromptStrategy)

        prompt = STRATEGY_PROMPT.format(
            user_input=state["user_input"]
        )

        strategy = structured_llm.invoke(
            [
                ("system", SYSTEM_PROMPT),
                HumanMessage(content=prompt)
            ]
        )

        logger.info("Detected intent: %s", strategy.intent)
        logger.info(
            "Strategy selected:\n%s",
            strategy.model_dump_json(indent=2),
        )

        state["strategy"] = strategy

        return state


# Node 2 - Build Prompt
def build_dynamic_prompt(state: AgentState) -> AgentState:
    """
    Build the final prompt
    """
    with ExecutionTracker("Build Dynamic Prompt"):
        logger.info("Building prompt...")

        prompt = build_prompt(
            strategy=state["strategy"],
            user_input=state["user_input"],
        )

        validate_prompt(prompt)

        state["final_prompt"] = prompt

        logger.debug(
            "Generated Prompt:\n%s",
            state["final_prompt"],
        )

        return state 


# Node 3 - Generate Response
def generate_response(state: AgentState) -> AgentState:
    """
    Execute the synthesized prompt.
    """
    with ExecutionTracker("Generate Response"):
        logger.info("Generating response...")

        response = llm.invoke(
            state["final_prompt"]
        )

        state["response"] = response.content

        return state