from dataclasses import dataclass
from typing import Callable, Type

from pydantic import BaseModel


@dataclass
class Tool:
    name: str
    description: str
    schema: Type[BaseModel]
    handler: Callable

    category: str = "general"

    risk_level: str = "low"
    timeout: int = 10
    enabled: bool = True
    requires_approval: bool = False