import sys
from rich.console import Console

from app.agent import run_agent

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

console = Console()


def main():

    console.print("\n[bold cyan]🤖 Tool Calling Agent[/bold cyan] [magenta]• type 'exit' to quit[/magenta]\n")

    while True:

        try:

            user_input = console.input("[bold cyan]You › [/bold cyan]").strip()

            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit"):
                console.print("\n[magenta]Goodbye! 👋[/magenta]\n")
                break

            response = run_agent(user_input)

            console.print(f"\n[bold magenta]Agent › [/bold magenta][magenta]{response}[/magenta]\n")

        except (KeyboardInterrupt, EOFError):
            console.print("\n[magenta]Session ended.[/magenta]\n")
            break

        except Exception as e:

            console.print(f"\n[bold magenta]Error › [/bold magenta][magenta]{e}[/magenta]\n")


if __name__ == "__main__":
    main()