"""UI module for Safe SQL Agent using Rich (2 colors: Cyan & White, No Boxes)."""

from rich.console import Console
from rich.table import Table

console = Console()


def display_rich_output(final_state: dict):
    console.print()
    console.print("[bold cyan]DAY 08[/bold cyan] [dim white]|[/dim white] [bold white]SAFE SQL AGENT[/bold white]\n")


    question = final_state.get("question", "")
    console.print(f"[bold cyan]User Question:[/bold cyan] [white]{question}[/white]\n")

    generated_sql = final_state.get("generated_sql", "")
    if generated_sql:
        console.print("[bold cyan]Generated SQL:[/bold cyan]")
        for line in generated_sql.strip().splitlines():
            console.print(f"  [white]{line}[/white]")
        console.print()

    val_res = final_state.get("validation_result")
    if val_res:
        status_str = "[bold cyan]PASSED[/bold cyan]" if val_res.allowed else "[bold white]FAILED[/bold white]"
        console.print(f"[bold cyan]Guardrail Check:[/bold cyan] {status_str}")
        if val_res.errors:
            for err in val_res.errors:
                console.print(f"  [dim white]•[/dim white] [white]{err}[/white]")
        console.print()

    exec_res = final_state.get("execution_result")
    if exec_res is not None:
        console.print("[bold cyan]Execution Results:[/bold cyan]")
        if isinstance(exec_res, list) and len(exec_res) > 0 and isinstance(exec_res[0], dict):
            table = Table(box=None, header_style="bold cyan", show_edge=False, pad_edge=False)
            headers = list(exec_res[0].keys())
            for header in headers:
                table.add_column(header)
            for row in exec_res:
                table.add_row(*[str(row[h]) for h in headers], style="white")
            console.print(table)
        else:
            console.print(f"  [white]{exec_res}[/white]")
        console.print()

    error = final_state.get("error")
    if error and exec_res is None:
        console.print(f"[bold cyan]Status Error:[/bold cyan] [white]{error}[/white]\n")
