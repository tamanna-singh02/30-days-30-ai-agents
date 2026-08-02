from typing import Any, Dict

class BasePromptTemplate:
    """
    Base class for prompt formatting.
    """
    def __init__(self, template: str):
        self.template = template

    def format(self, **kwargs: Any) -> str:
        return self.template.format(**kwargs)
