"""
Utility functions for the Dynamic Prompt Synthesizer using Rich formatting.
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from .config import MAX_PROMPT_LENGTH

from agents.day_02_dynamic_prompt_synthesizer.schemas import PromptStrategy

console = Console()

def validate_prompt(prompt: str) -> None:
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")
    if len(prompt) > MAX_PROMPT_LENGTH:
        raise ValueError(f"Prompt is too long. Maximum length is {MAX_PROMPT_LENGTH} characters.")

def display_strategy(strategy: PromptStrategy) -> None:
    """Display the prompt engineering strategy in a Rich Table."""
    table = Table(
        title="[bold cyan]Prompt Strategy[/bold cyan]",
        border_style="cyan",
        show_header=True,
        header_style="bold cyan"
    )
    table.add_column("Parameter", style="cyan", width=20)
    table.add_column("Value", style="yellow")

    table.add_row("Intent", strategy.intent.capitalize())
    table.add_row("Tone", strategy.tone)
    table.add_row("Output Format", strategy.output_format)
    table.add_row("Constraints", ", ".join(strategy.constraints) if strategy.constraints else "None")

    console.print(table)


def display_synthesized_prompt(prompt: str) -> None:
    """Display the synthesized prompt in a Rich Panel."""
    console.print(
        Panel(
            prompt,
            title="[bold cyan]Synthesized Prompt[/bold cyan]",
            border_style="cyan",
            expand=True
        )
    )


def display_generated_response(response: str) -> None:
    """Display the final LLM response rendered as Rich Markdown."""
    console.print(
        Panel(
            Markdown(response),
            title="[bold cyan]LLM Response[/bold cyan]",
            border_style="cyan",
            expand=True
        )
    )
