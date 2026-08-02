"""
Day 01 - Structured Data Extractor Agent package.
"""

def __getattr__(name: str):
    if name == "run_agent":
        from agents.day_01_structured_output.agent import run_agent
        return run_agent
    elif name == "display_rich_output":
        from agents.day_01_structured_output.ui import display_rich_output
        return display_rich_output
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["run_agent", "display_rich_output"]
