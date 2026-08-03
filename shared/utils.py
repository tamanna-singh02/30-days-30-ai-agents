import time
from typing import Optional, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown

console = Console()

class ExecutionTracker:
    """
    Context manager to track execution time, latency, and success/failure status.
    """

    def __init__(self, name: str = ""):
        self.name = name
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.latency_seconds: float = 0.0

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        if self.start_time:
            self.latency_seconds = round(self.end_time - self.start_time, 4)
        if self.name:
            from shared.logger import logger
            logger.info("%s completed in %ss", self.name, self.latency_seconds)


def print_header(title: str, subtitle: Optional[str] = None) -> None:
    """Prints a styled header for CLI agent execution using Rich."""
    grid = Table.grid(expand=True)
    grid.add_column(justify="center")
    grid.add_row(f"[bold cyan]{title}[/bold cyan]")
    if subtitle:
        grid.add_row(f"[dim]{subtitle}[/dim]")
    console.print(Panel(grid, border_style="cyan", expand=True))


def print_panel(content: Any, title: str = "", border_style: str = "blue", subtitle: str = "") -> None:
    """Prints content wrapped in a Rich panel."""
    console.print(Panel(content, title=f"[bold]{title}[/bold]", subtitle=subtitle, border_style=border_style, expand=True))


def print_markdown(content: str, title: str = "", border_style: str = "green") -> None:
    """Renders markdown inside a Rich panel."""
    md = Markdown(content)
    console.print(Panel(md, title=f"[bold]{title}[/bold]", border_style=border_style, expand=True))
