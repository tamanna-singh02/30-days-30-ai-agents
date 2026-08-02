import os
import sys
from typing import Any, Dict

# Ensure UTF-8 output encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from rich.rule import Rule

from shared.logger import logger
from shared.utils import ExecutionTracker
from agents.day_01_structured_output.graph import build_graph
from agents.day_01_structured_output.ui import console, display_rich_output

def run_agent(text: str, show_ui: bool = False) -> Dict[str, Any]:
    """
    Executes the structured data extractor agent workflow over the input text.
    """
    workflow = build_graph()

    initial_state = {
        "input_text": text,
        "retry_count": 0,
        "raw_response": None,
        "validation_error": None,
        "final_profile": None,
    }

    with ExecutionTracker() as tracker:
        result = workflow.invoke(initial_state)

    logger.info(f"Execution Time: {tracker.latency_seconds}s")
    
    if show_ui:
        display_rich_output(result, tracker.latency_seconds)

    return result

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)

    console.print(Rule("[bold yellow]1. Running Standard Resume (Expected: 0 Retries)[/bold yellow]", style="yellow"))
    sample_path = os.path.join(base_dir, "sample_resume.txt")
    with open(sample_path, "r", encoding="utf-8") as f:
        resume_standard = f.read()
    run_agent(resume_standard, show_ui=True)

    console.print(Rule("[bold yellow]2. Running Resume with Retries & Self-Correction[/bold yellow]", style="yellow"))
    retry_sample_path = os.path.join(base_dir, "sample_resume_retry.txt")
    if os.path.exists(retry_sample_path):
        with open(retry_sample_path, "r", encoding="utf-8") as f:
            resume_retry = f.read()
        run_agent(resume_retry, show_ui=True)