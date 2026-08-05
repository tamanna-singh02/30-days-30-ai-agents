"""
Application entry point for Map-Reduce Summarizer.
"""

import os
import sys
import time
from agents.day_04_map_reduce_summarizer.graph import graph
from agents.day_04_map_reduce_summarizer.config import INPUT_FILE, OUTPUT_FILE
from agents.day_04_map_reduce_summarizer.ui import display_rich_output


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_FILE

    start_time = time.perf_counter()
    result = graph.invoke({"file_path": file_path})
    execution_time = time.perf_counter() - start_time

    final_summary = result.get("final_summary", "")

    # Save summary artifact to output file
    output_path = OUTPUT_FILE
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(final_summary)

    # Render rich aesthetic output
    display_rich_output(result, execution_time, output_path)


if __name__ == "__main__":
    main()