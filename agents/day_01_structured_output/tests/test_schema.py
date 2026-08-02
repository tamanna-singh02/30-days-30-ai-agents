import pytest
from pydantic import ValidationError
from agents.day_01_structured_output.schemas import CandidateProfile

def test_valid_candidate_profile():
    profile = CandidateProfile(
        full_name="Tamanna Singh",
        years_experience=2,
        primary_skills=["Python", "LangGraph", "React"],
        highest_degree="B.E.",
        is_hireable=True,
    )
    assert profile.full_name == "Tamanna Singh"
    assert profile.years_experience == 2
    assert profile.is_hireable is True

def test_invalid_candidate_profile_schema():
    with pytest.raises(ValidationError):
        CandidateProfile(
            full_name="Tamanna Singh",
            years_experience="invalid_int", # Invalid type
            primary_skills=["Python"],
            is_hireable=True,
        )
