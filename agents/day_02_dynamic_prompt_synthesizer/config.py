from typing import Final

TEMPERATURE: Final[float] = 0.2

DEFAULT_TONE: Final[str] = "Professional"
DEFAULT_OUTPUT_FORMAT: Final[str] = "Markdown"

MAX_CONTRAINTS: Final[int] = 5
MAX_PROMPT_LENGTH: Final[int] = 4000

SUPPORTED_INTENTS: Final[set[str]] = [
    "email",
    "summarization",
    "extraction"
]