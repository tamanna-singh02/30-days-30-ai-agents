"""
Rich Terminal UI components for Day 01 — Structured Data Extractor.
"""

from typing import Any, Dict
from rich.console import Console
from rich.rule import Rule
from rich.table import Table

from agents.day_01_structured_output.schemas import CandidateProfile

console = Console()


def display_rich_output(result: Dict[str, Any], latency_seconds: float) -> None:
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
