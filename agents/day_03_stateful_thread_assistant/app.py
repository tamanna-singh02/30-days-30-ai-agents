import os
import sys

AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(AGENT_DIR, "..", ".."))

if AGENT_DIR not in sys.path:
    sys.path.insert(0, AGENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from langchain_core.messages import HumanMessage
from graphs.assistant_graph import graph

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()

def display_banner(thread_id: str):
    banner_text = Text()
    banner_text.append("Stateful Thread Assistant", style="bold cyan")
    banner_text.append("\nThread ID: ", style="dim cyan")
    banner_text.append(thread_id, style="bold white")
    
    console.print(
        Panel(
            banner_text,
            border_style="cyan",
            expand=False,
            padding=(0, 3)
        )
    )

def format_memory_table(memory: dict) -> Table:
    table = Table(show_header=True, header_style="bold cyan", border_style="dim cyan", box=None, pad_edge=False)
    table.add_column("Attribute", style="cyan")
    table.add_column("Stored Value", style="white")

    active_items = {k: v for k, v in memory.items() if v}
    if not active_items:
        table.add_row("(empty)", "(no memory recorded yet)", style="dim")
    else:
        for k, v in active_items.items():
            val_str = ", ".join(v) if isinstance(v, list) else str(v)
            table.add_row(k.capitalize(), val_str)

    return table

def format_diff_summary(state_diff: dict) -> str:
    if not state_diff:
        return "[dim]No changes in this turn[/dim]"
    
    diff_parts = []
    for k, v in state_diff.items():
        new_val = v.get("new")
        val_display = ", ".join(new_val) if isinstance(new_val, list) else str(new_val)
        diff_parts.append(f"[bold cyan]+ {k}[/bold cyan]: {val_display}")
    return " | ".join(diff_parts)

def main():
    console.clear()
    thread_id = console.input("[bold cyan]Thread ID[/bold cyan] [dim](default: main_thread)[/dim]: ").strip()
    if not thread_id:
        thread_id = "main_thread"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    display_banner(thread_id)
    console.print("[dim cyan]Type '[bold white]exit[/bold white]' to quit.[/dim cyan]\n")

    while True:
        try:
            user_input = console.input("[bold cyan]You > [/bold cyan]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim cyan]Session closed.[/dim cyan]")
            break

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            console.print("[dim cyan]Goodbye![/dim cyan]")
            break

        with console.status("[cyan]Processing message...[/cyan]", spinner="dots"):
            result = graph.invoke(
                {
                    "messages": [HumanMessage(content=user_input)],
                    "memory": {},
                    "previous_memory": {},
                    "state_diff": {}
                },
                config=config
            )

        ai_response = result["messages"][-1].content
        current_memory = result.get("memory", {})
        state_diff = result.get("state_diff", {})
        versions = result.get("memory_versions", [])

        # 1. AI Assistant Panel
        console.print(
            Panel(
                ai_response,
                title="[bold cyan]Assistant[/bold cyan]",
                title_align="left",
                border_style="cyan",
                padding=(1, 2)
            )
        )

        # 2. State & Memory Panel
        memory_table = format_memory_table(current_memory)
        diff_summary = format_diff_summary(state_diff)

        console.print(
            Panel(
                memory_table,
                title=f"[bold cyan]Stateful User Memory (v{len(versions)})[/bold cyan]",
                subtitle=f"[dim cyan]Diff: {diff_summary}[/dim cyan]",
                border_style="dim cyan",
                padding=(0, 2)
            )
        )
        console.print()

if __name__ == "__main__":
    main()