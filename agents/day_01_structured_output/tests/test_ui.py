from unittest.mock import patch
from agents.day_01_structured_output.schemas import CandidateProfile
from agents.day_01_structured_output.ui import display_rich_output, console


def test_display_rich_output_success():
    profile = CandidateProfile(
        full_name="John Doe",
        years_experience=5,
        highest_degree="Master of Science",
        primary_skills=["Python", "FastAPI", "Docker"],
        is_hireable=True,
    )
    result = {
        "final_profile": profile,
        "retry_count": 0,
        "validation_error": None,
    }
    with patch.object(console, "print") as mock_print:
        display_rich_output(result, 1.23)
        assert mock_print.called


def test_display_rich_output_failure():
    result = {
        "final_profile": None,
        "retry_count": 3,
        "validation_error": "Validation failed",
    }
    with patch.object(console, "print") as mock_print:
        display_rich_output(result, 2.45)
        assert mock_print.called
