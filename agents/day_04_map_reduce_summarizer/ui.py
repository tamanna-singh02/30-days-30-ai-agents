"""
Rich Terminal UI components for Day 04 — Map-Reduce Document Summarizer.
"""

import sys
from typing import Any, Dict
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.markdown import Markdown

# Safe UTF-8 console output handling for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

console = Console()


def display_rich_output(result: Dict[str, Any], execution_time: float, output_path: str) -> None:
    """
    Renders map-reduce document metrics and final markdown summary in a clean, high-aesthetic layout.
    """
    file_path = result.get("file_path", "N/A")
    token_count = result.get("token_count", 0)
    chunk_count = result.get("chunk_count", len(result.get("chunks", [])))
    avg_tokens = result.get("avg_tokens_per_chunk", 0.0)
    largest_chunk = result.get("largest_chunk", 0)
    smallest_chunk = result.get("smallest_chunk", 0)
    final_summary = result.get("final_summary", "")

    console.print()
    console.print(Rule("[bold cyan]Day 04 — Map-Reduce Document Summarizer[/bold cyan]", style="cyan"))
    console.print("  [dim cyan]LangGraph  |  Token-Aware Chunking  |  Map-Reduce Synthesis[/dim cyan]\n")

    # Document Metrics Table
    table = Table(box=None, padding=(0, 2), show_header=False)
    table.add_column("Metric", style="bold cyan", justify="left", width=26)
    table.add_column("Value", style="white", justify="left")

    table.add_row("Document Path", file_path)
    table.add_row("Total Tokens", f"{token_count:,}")
    table.add_row("Total Chunks", str(chunk_count))
    table.add_row("Average Tokens / Chunk", f"{avg_tokens:.1f}")
    table.add_row("Largest Chunk", f"{largest_chunk:,} tokens")
    table.add_row("Smallest Chunk", f"{smallest_chunk:,} tokens")
    table.add_row("Execution Time", f"{execution_time:.2f}s")

    console.print(table)
    console.print()

    # Final Summary Markdown Panel
    if final_summary:
        summary_markdown = Markdown(final_summary)
        console.print(
            Panel(
                summary_markdown,
                title="[bold cyan]FINAL SYNTHESIZED SUMMARY[/bold cyan]",
                title_align="left",
                border_style="cyan",
                padding=(1, 2),
            )
        )
    else:
        console.print("[bold red]No summary generated.[/bold red]")

    console.print()
    console.print(Rule(style="cyan"))
    console.print(f"  [bold green][OK] Summary saved to [/bold green][bold white]{output_path}[/bold white]")
    console.print(Rule(style="cyan"))
    console.print()
