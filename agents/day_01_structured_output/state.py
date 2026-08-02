from typing import Any, Optional, TypedDict
from agents.day_01_structured_output.schemas import CandidateProfile

class ExtractorState(TypedDict):
    """
    State definition for the structured extraction workflow graph.
    """
    input_text: str
    retry_count: int
    raw_response: Optional[Any]
    validation_error: Optional[str]
    final_profile: Optional[CandidateProfile]
