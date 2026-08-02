import os
import sys
from typing import Any, Dict

# Ensure UTF-8 output encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from rich.console import Console
from rich.rule import Rule
from rich.table import Table

from shared.logger import logger
from shared.utils import ExecutionTracker
from agents.day_01_structured_output.graph import build_graph
from agents.day_01_structured_output.schemas import CandidateProfile

console = Console()

def display_rich_output(result: Dict[str, Any], latency_seconds: float):
    """
    Renders candidate profile and workflow metrics in a clean, minimalist aesthetic without heavy boxes.
    """
    profile: CandidateProfile = result.get("final_profile")
    retry_count = result.get("retry_count", 0)
    validation_error = result.get("validation_error")

    console.print()
    console.print(Rule("[bold cyan]Day 01 — Structured Data Extractor[/bold cyan]", style="cyan"))
    console.print("  [dim cyan]LangGraph  •  Pydantic  •  Groq[/dim cyan]\n")

    if profile:
        table = Table(box=None, padding=(0, 2), show_header=False)
        table.add_column("Field", style="bold cyan", justify="left", width=22)
        table.add_column("Value", style="white", justify="left")

        table.add_row("Full Name", profile.full_name)
        table.add_row("Years of Experience", str(profile.years_experience))
        table.add_row("Highest Degree", profile.highest_degree or "N/A")
        table.add_row("Primary Skills", ", ".join(profile.primary_skills))
        table.add_row("Is Hireable?", "YES" if profile.is_hireable else "NO")

        console.print(table)
    elif validation_error:
        console.print(f"  [bold cyan]Extraction Failed:[/bold cyan] [white]{validation_error}[/white]")

    console.print()
    console.print(Rule(style="cyan"))
    status_str = "[bold cyan]SUCCESS[/bold cyan]" if profile else "[white]FAILED[/white]"
    console.print(
        f"  [bold cyan]Latency:[/bold cyan] {latency_seconds}s    "
        f"[bold cyan]Retries:[/bold cyan] {retry_count}    "
        f"[bold cyan]Status:[/bold cyan] {status_str}"
    )
    console.print(Rule(style="cyan"))
    console.print()

def run_agent(text: str, show_ui: bool = False) -> Dict[str, Any]:
    """
    Executes the structured data extractor agent workflow over the input text.
    """
    workflow = build_graph()

    initial_state = {
        "input_text": text,
        "retry_count": 0,
        "raw_response": None,
        "validation_error": None,
        "final_profile": None,
    }

    with ExecutionTracker() as tracker:
        result = workflow.invoke(initial_state)

    logger.info(f"Execution Time: {tracker.latency_seconds}s")
    
    if show_ui:
        display_rich_output(result, tracker.latency_seconds)

    return result

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)

    console.print(Rule("[bold yellow]1. Running Standard Resume (Expected: 0 Retries)[/bold yellow]", style="yellow"))
    sample_path = os.path.join(base_dir, "sample_resume.txt")
    with open(sample_path, "r", encoding="utf-8") as f:
        resume_standard = f.read()
    run_agent(resume_standard, show_ui=True)

    console.print(Rule("[bold yellow]2. Running Resume with Retries & Self-Correction[/bold yellow]", style="yellow"))
    retry_sample_path = os.path.join(base_dir, "sample_resume_retry.txt")
    if os.path.exists(retry_sample_path):
        with open(retry_sample_path, "r", encoding="utf-8") as f:
            resume_retry = f.read()
        run_agent(resume_retry, show_ui=True)