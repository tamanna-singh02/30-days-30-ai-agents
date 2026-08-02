import os
from shared.config import LANGCHAIN_TRACING_V2, LANGCHAIN_API_KEY, LANGCHAIN_PROJECT
from shared.logger import logger

def setup_tracing() -> bool:
    """
    Sets up LangChain / LangSmith tracing environment variables if enabled.
    """
    if LANGCHAIN_TRACING_V2.lower() == "true":
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        if LANGCHAIN_API_KEY:
            os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
        if LANGCHAIN_PROJECT:
            os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT
        logger.info(f"LangChain tracing enabled for project: {LANGCHAIN_PROJECT}")
        return True
    return False
