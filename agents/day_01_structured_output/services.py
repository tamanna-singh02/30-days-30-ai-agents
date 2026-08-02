from shared.llm import get_llm
from shared.config import MODEL_NAME, MODEL_PROVIDER, TEMPERATURE
from agents.day_01_structured_output.schemas import CandidateProfile

def get_structured_llm():
    """
    Returns the configured LLM with structured output enabled for CandidateProfile.
    """
    llm = get_llm(
        provider=MODEL_PROVIDER,
        model=MODEL_NAME,
        temperature=TEMPERATURE,
    )

    return llm.with_structured_output(
        CandidateProfile,
        include_raw=False,
    )
