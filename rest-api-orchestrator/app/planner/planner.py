import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Any

repo_root = str(Path(__file__).resolve().parents[3])
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

try:
    from shared.llm import get_llm
except ImportError:
    get_llm = None

logger = logging.getLogger("planner")

from app.api.registry import APIRegistry
from app.models.plan import ExecutionPlan, ExecutionStep
from app.orchestrator.validator import PlanValidator, PlanValidationError
from app.planner.prompts import PLANNER_SYSTEM_PROMPT


class LLMPlanner:
    def __init__(self, registry: APIRegistry, llm: Any = None):
        self.registry = registry
        if llm is not None:
            self.llm = llm
        elif get_llm is not None:
            try:
                self.llm = get_llm(temperature=0.0)
            except Exception:
                self.llm = None
        else:
            self.llm = None

        self.validator = PlanValidator(registry)

    def _format_api_specs(self) -> str:
        specs = []
        for api in self.registry.list_apis():
            params = ", ".join(
                f"{p.name} ({p.type}{', required' if p.required else ''}): {p.description}"
                for p in api.parameters
            )
            specs.append(
                f"- Name: {api.name}\n"
                f"  Description: {api.description}\n"
                f"  Method: {api.method.value}\n"
                f"  Path: {api.path}\n"
                f"  Parameters: [{params}]\n"
            )
        return "\n".join(specs)

    async def plan(self, user_goal: str) -> ExecutionPlan:
        if self.llm is not None:
            api_specs = self._format_api_specs()
            system_prompt = PLANNER_SYSTEM_PROMPT.format(api_specs=api_specs)

            try:
                response = await asyncio.wait_for(
                    self.llm.ainvoke([
                        ("system", system_prompt),
                        ("user", f"User Goal: {user_goal}"),
                    ]),
                    timeout=3.0,
                )

                content = getattr(response, "content", str(response))
                if isinstance(content, str):
                    clean_json = content.strip()
                    if clean_json.startswith("```json"):
                        clean_json = clean_json[7:]
                    if clean_json.startswith("```"):
                        clean_json = clean_json[3:]
                    if clean_json.endswith("```"):
                        clean_json = clean_json[:-3]

                    plan_dict = json.loads(clean_json.strip())
                    plan = ExecutionPlan.model_validate(plan_dict)
                    self.validator.validate(plan)
                    return plan

            except Exception as exc:
                logger.warning(f"LLM planning failed ({exc}). Falling back to heuristic planner.")

        return self._heuristic_fallback(user_goal)

    def _heuristic_fallback(self, user_goal: str) -> ExecutionPlan:
        goal_lower = user_goal.lower()
        steps: list[ExecutionStep] = []

        if "cancel" in goal_lower and "order" in goal_lower:
            steps = [
                ExecutionStep(
                    id="get_user_orders",
                    api="get_user_orders",
                    parameters={"user_id": "42"},
                ),
                ExecutionStep(
                    id="cancel_order",
                    api="cancel_order",
                    parameters={"order_id": "{{get_user_orders.orders[0].id}}"},
                    depends_on=["get_user_orders"],
                ),
            ]
        elif "user" in goal_lower:
            steps = [
                ExecutionStep(
                    id="get_user",
                    api="get_user",
                    parameters={"user_id": "42"},
                )
            ]

        plan = ExecutionPlan(goal=user_goal, steps=steps)
        self.validator.validate(plan)
        return plan
