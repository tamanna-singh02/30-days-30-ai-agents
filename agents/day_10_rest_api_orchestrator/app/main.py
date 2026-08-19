import asyncio
import sys
import httpx
from rich.console import Console
from rich.table import Table

from app.api.client import APIClient
from app.api.schemas import create_api_registry
from app.models.plan import ExecutionPlan, ExecutionStep
from app.orchestrator.engine import Orchestrator
from app.planner.planner import LLMPlanner

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Strict 2-color palette: Cyan & Green
PRIMARY_COLOR = "cyan"
ACCENT_COLOR = "green"

console = Console()


def create_mock_transport() -> httpx.MockTransport:
    """
    Creates an in-process httpx MockTransport to simulate REST API responses.
    """
    def handler(request: httpx.Request) -> httpx.Response:
        url_path = request.url.path
        method = request.method

        if method == "GET" and url_path.startswith("/users/42/orders"):
            return httpx.Response(
                200,
                json={
                    "orders": [
                        {"id": "ord_9981", "status": "pending", "amount": 149.99},
                        {"id": "ord_9982", "status": "completed", "amount": 49.50},
                    ]
                },
            )
        elif method == "GET" and url_path.startswith("/users/42"):
            return httpx.Response(
                200,
                json={
                    "id": 42,
                    "name": "Jane Doe",
                    "email": "jane.doe@example.com",
                },
            )
        elif method == "POST" and "/cancel" in url_path:
            order_id = url_path.split("/")[2]
            return httpx.Response(
                200,
                json={
                    "success": True,
                    "message": f"Order {order_id} successfully cancelled.",
                },
            )

        return httpx.Response(404, json={"error": "Not Found"})

    return httpx.MockTransport(handler)


async def main():
    console.rule(f"[bold {PRIMARY_COLOR}]🤖 Day 10: REST API Orchestrator[/bold {PRIMARY_COLOR}]")

    # 1. Initialize API Registry
    registry = create_api_registry()
    console.print(f"[{ACCENT_COLOR}]✓ Registered {len(registry.list_apis())} API endpoints in Registry[/{ACCENT_COLOR}]\n")

    table = Table(title="Available API Registry")
    table.add_column("Name", style=PRIMARY_COLOR)
    table.add_column("Method", style=ACCENT_COLOR)
    table.add_column("Path", style=PRIMARY_COLOR)
    table.add_column("Description", style=ACCENT_COLOR)

    for api in registry.list_apis():
        table.add_row(api.name, api.method.value, api.path, api.description)
    console.print(table)
    console.print()

    # 2. Setup Client with Mock Transport for Standalone Execution
    mock_transport = create_mock_transport()
    async_client = httpx.AsyncClient(transport=mock_transport, base_url="http://mock-api.local")
    client = APIClient(base_url="http://mock-api.local")
    client.execute = lambda api, params: _mock_execute(async_client, api, params)

    # 3. Create Plan using LLMPlanner (with fallback)
    planner = LLMPlanner(registry=registry)
    goal = "Find the user's pending order and cancel the latest one"
    console.print(f"[bold {PRIMARY_COLOR}]Target Goal:[/bold {PRIMARY_COLOR}] [{ACCENT_COLOR}]{goal}[/{ACCENT_COLOR}]\n")

    plan = await planner.plan(goal)
    console.print(f"[bold {PRIMARY_COLOR}]Synthesized Plan ({len(plan.steps)} steps):[/bold {PRIMARY_COLOR}]")
    for idx, step in enumerate(plan.steps, 1):
        console.print(f"  {idx}. [{PRIMARY_COLOR}]{step.id}[/{PRIMARY_COLOR}] -> API: [{ACCENT_COLOR}]{step.api}[/{ACCENT_COLOR}] (depends_on={step.depends_on})")
    console.print()

    # 4. Execute Plan using Orchestrator Engine
    orchestrator = Orchestrator(registry=registry, client=client)
    console.print(f"[bold {PRIMARY_COLOR}]Executing Orchestration Pipeline...[/bold {PRIMARY_COLOR}]")
    state = await orchestrator.execute(plan)

    # 5. Output Execution Results
    console.print(f"\n[bold {PRIMARY_COLOR}]Execution Summary:[/bold {PRIMARY_COLOR}]")
    for step_id, result in state.results.items():
        console.print(f"  • Step [{PRIMARY_COLOR}]{step_id}[/{PRIMARY_COLOR}]: [{ACCENT_COLOR}]{result.status.value.upper()}[/{ACCENT_COLOR}] (HTTP {result.status_code})")
        console.print(f"    Data: [{ACCENT_COLOR}]{result.data}[/{ACCENT_COLOR}]\n")


async def _mock_execute(async_client: httpx.AsyncClient, api, parameters):
    path = api.path
    for name, value in parameters.items():
        path = path.replace(f"{{{name}}}", str(value))
    
    url = f"http://mock-api.local{path}"
    response = await async_client.request(method=api.method.value, url=url)
    try:
        data = response.json()
    except Exception:
        data = response.text
    return response.status_code, data


if __name__ == "__main__":
    asyncio.run(main())