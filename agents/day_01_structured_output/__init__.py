"""
Day 01 - Structured Data Extractor Agent package.
"""

def __getattr__(name: str):
    if name == "run_agent":
        from agents.day_01_structured_output.agent import run_agent
        return run_agent
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["run_agent"]
