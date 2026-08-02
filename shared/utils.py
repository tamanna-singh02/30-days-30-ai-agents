import time
from typing import Optional

class ExecutionTracker:
    """
    Context manager to track execution time, latency, and success/failure status.
    """

    def __init__(self):
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
