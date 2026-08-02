import logging
import sys

def setup_logger(name: str = "ai_agents") -> logging.Logger:
    """
    Sets up a standardized logger for the project using rich if available.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        try:
            from rich.logging import RichHandler
            handler = RichHandler(
                rich_tracebacks=True,
                show_time=True,
                show_path=False,
                markup=True,
            )
            formatter = logging.Formatter("%(message)s")
        except ImportError:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

logger = setup_logger()
