"""
Entry point for the prompt synthesizer application with Rich formatting.
"""

from rich.console import Console
from rich.prompt import Prompt

from shared.utils import print_header
from agents.day_02_dynamic_prompt_synthesizer.graph import graph
from agents.day_02_dynamic_prompt_synthesizer.utils import (
    display_strategy,
    display_synthesized_prompt,
    display_generated_response,
)

console = Console()

def main() -> None:
    print_header("Day 02: Dynamic Prompt Synthesizer 🎯", "30 Days of AI Agents - LangGraph & Rich")

    user_input = Prompt.ask("\n[bold yellow]Enter your request[/bold yellow]")

    if not user_input.strip():
        console.print("[red]No request entered. Exiting.[/red]")
        return

    with console.status("[bold cyan]Synthesizing prompt & generating response...[/bold cyan]", spinner="dots"):
        result = graph.invoke({
            "user_input": user_input
        })

    console.print()
    if "strategy" in result and result["strategy"]:
        display_strategy(result["strategy"])
        console.print()

    if "final_prompt" in result and result["final_prompt"]:
        display_synthesized_prompt(result["final_prompt"])
        console.print()

    if "response" in result and result["response"]:
        display_generated_response(result["response"])

if __name__ == "__main__":
    main()
