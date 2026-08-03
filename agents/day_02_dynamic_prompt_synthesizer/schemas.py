from typing import Literal
from pydantic import BaseModel, Field

class PromptStrategy(BaseModel):

    intent: Literal[
        "email",
        "summarization",
        "extraction"
    ]

    tone: str = Field(
        description="Desired tone of the output"
    )

    output_format: str = Field(
        description="Preferred output format."
    )

    constraints: list[str] = Field(
        default_factory=list,
        description="Extra instructions for the generated response."
    )

    class PromptResponse(BaseModel):
        """Final synthesized prompt."""

        prompt: str