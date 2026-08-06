import sys
import os
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

agent_dir = Path(__file__).resolve().parent
root_dir = agent_dir.parent.parent

if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
if str(agent_dir) not in sys.path:
    sys.path.insert(0, str(agent_dir))

from langchain_core.messages import HumanMessage
from rich.console import Console
from rich.rule import Rule

from graphs.assistant_graph import graph
from memory.memory_manager import memory_manager

console = Console()

console.print()
console.print(Rule("[bold cyan]Persistent Semantic Memory Agent[/bold cyan]", style="dim cyan"))
console.print("[dim]Type 'exit' to stop.[/dim]\n")

while True:
    try:
        user = console.input("[bold cyan]You › [/bold cyan]").strip()
    except (KeyboardInterrupt, EOFError):
        console.print("\n[dim]Goodbye![/dim]\n")
        break

    if not user:
        continue

    if user.lower() in ("exit", "quit", "q", "bye"):
        console.print("\n[dim]Goodbye![/dim]\n")
        break

    with console.status("[dim cyan]Thinking...[/dim cyan]", spinner="dots"):
        result = graph.invoke(
            {
                "messages": [
                    HumanMessage(content=user)
                ]
            }
        )

    response_text = result.get("response", "")
    console.print()
    console.print("[bold cyan]Assistant[/bold cyan]")
    console.print(response_text)
    console.print()

    facts = memory_manager.list_all_facts()
    vector_count = memory_manager.count_vector_memories()

    console.print("[bold cyan]=== Extracted & Saved Memories ===[/bold cyan]")
    if facts:
        for fact in facts:
            console.print(f"  [cyan]• Key:[/cyan] {fact.key} [dim]|[/dim] [cyan]Value:[/cyan] {fact.value}")
    else:
        console.print("  [dim]No structured facts saved yet.[/dim]")

    console.print(f"  [cyan]• Vector Store Entries:[/cyan] {vector_count}")
    console.print(Rule(style="dim cyan"))
    console.print()
