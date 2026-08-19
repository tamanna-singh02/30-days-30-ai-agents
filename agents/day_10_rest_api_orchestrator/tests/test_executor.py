import pytest
from app.api.schemas import create_api_registry
from app.models.plan import ExecutionStep
from app.orchestrator.resolver import ReferenceResolver
from app.orchestrator.state import ExecutionState, StepResult, StepStatus


def test_reference_resolver_nested_lists_and_dicts():
    state = ExecutionState()
    state.add_result(
        StepResult(
            step_id="step1",
            status=StepStatus.SUCCESS,
            status_code=200,
            data={
                "users": [
                    {"id": 101, "meta": {"role": "admin"}},
                    {"id": 102, "meta": {"role": "user"}},
                ]
            },
        )
    )

    resolver = ReferenceResolver(state)
    assert resolver.resolve("{{step1.users[0].id}}") == 101
    assert resolver.resolve("{{step1.users[1].meta.role}}") == "user"
    assert resolver.resolve("static_val") == "static_val"
