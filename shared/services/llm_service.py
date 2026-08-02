from typing import Any, Type
from pydantic import BaseModel
from shared.llm import get_llm

class LLMService:
    """
    Service wrapper around LLM calls.
    """

    def __init__(self, provider: str = None, model: str = None, temperature: float = 0.0):
        self.llm = get_llm(provider=provider, model=model, temperature=temperature)

    def get_structured_llm(self, schema: Type[BaseModel]):
        return self.llm.with_structured_output(schema, include_raw=False)
