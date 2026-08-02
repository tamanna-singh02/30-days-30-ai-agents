from langchain_core.messages import HumanMessage

from shared.logger import logger
from shared.config import MAX_RETRIES

from agents.day_01_structured_output.state import ExtractorState
from agents.day_01_structured_output.schemas import CandidateProfile
from agents.day_01_structured_output.services import get_structured_llm
from agents.day_01_structured_output.prompts import (
    SYSTEM_PROMPT,
    build_extraction_prompt,
    build_retry_prompt,
)

def extract_node(state: ExtractorState):
    logger.info(f"Extractor Attempt: {state['retry_count'] + 1}")

    structured_llm = get_structured_llm()

    if state.get("validation_error"):
        prompt = build_retry_prompt(
            resume_text=state["input_text"],
            validation_error=state["validation_error"],
        )
    else:
        prompt = build_extraction_prompt(state["input_text"])

    try:
        response = structured_llm.invoke(
            [HumanMessage(content=f"{SYSTEM_PROMPT}\n\n{prompt}")]
        )
        return {
            "raw_response": response,
        }
    except Exception as e:
        logger.exception(e)
        return {
            "validation_error": str(e),
            "retry_count": state["retry_count"] + 1,
        }

def validate_node(state: ExtractorState):
    logger.info("Running Validation")

    response = state.get("raw_response")

    if response is None:
        return {
            "validation_error": "No response generated.",
            "retry_count": state["retry_count"] + 1,
        }

    if isinstance(response, CandidateProfile):
        logger.info("Validation PASSED.")
        return {
            "final_profile": response,
            "validation_error": None,
        }

    return {
        "validation_error": "Schema validation failed.",
        "retry_count": state["retry_count"] + 1,
    }

def route_validation(state: ExtractorState):
    if state.get("final_profile") is not None:
        return "success"

    if state.get("retry_count", 0) >= MAX_RETRIES:
        return "failure"

    return "retry"
