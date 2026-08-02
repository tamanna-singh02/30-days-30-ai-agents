from agents.day_01_structured_output.nodes import validate_node, route_validation
from agents.day_01_structured_output.schemas import CandidateProfile

def test_validate_node_success():
    profile = CandidateProfile(
        full_name="Tamanna Singh",
        years_experience=2,
        primary_skills=["Python", "LangGraph", "React"],
        highest_degree="B.E.",
        is_hireable=True,
    )
    state = {
        "input_text": "sample text",
        "retry_count": 0,
        "raw_response": profile,
        "validation_error": None,
        "final_profile": None,
    }

    res = validate_node(state)
    assert res.get("final_profile") == profile
    assert res.get("validation_error") is None

def test_validate_node_missing_response():
    state = {
        "input_text": "sample text",
        "retry_count": 0,
        "raw_response": None,
        "validation_error": None,
        "final_profile": None,
    }
    res = validate_node(state)
    assert res.get("validation_error") == "No response generated."
    assert res.get("retry_count") == 1

def test_route_validation_outcomes():
    profile = CandidateProfile(
        full_name="Tamanna Singh",
        years_experience=2,
        primary_skills=["Python"],
        highest_degree="B.E.",
        is_hireable=True,
    )

    success_state = {"final_profile": profile, "retry_count": 0}
    assert route_validation(success_state) == "success"

    retry_state = {"final_profile": None, "retry_count": 1}
    assert route_validation(retry_state) == "retry"

    failure_state = {"final_profile": None, "retry_count": 3}
    assert route_validation(failure_state) == "failure"
