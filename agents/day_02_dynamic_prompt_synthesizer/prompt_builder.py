import textwrap
from agents.day_02_dynamic_prompt_synthesizer.prompts import (
    EMAIL_TEMPLATE,
    EXTRACTION_TEMPLATE,
    SUMMARY_TEMPLATE,
    TRANSLATION_TEMPLATE,
    CODE_REVIEW_TEMPLATE
)

from agents.day_02_dynamic_prompt_synthesizer.schemas import PromptStrategy

TEMPLATE_MAP = {
    "email": EMAIL_TEMPLATE,
    "extraction": EXTRACTION_TEMPLATE,
    "summarization": SUMMARY_TEMPLATE,
    "translation": TRANSLATION_TEMPLATE,
    "code_review": CODE_REVIEW_TEMPLATE,
}

def build_prompt(strategy: PromptStrategy, user_input: str) -> str:
    """ Construct final prompt dynamically from sections. """

    template = TEMPLATE_MAP[strategy.intent].strip()

    sections = [
        template,
        f"Tone:\n{strategy.tone}",
        f"Output Format:\n{strategy.output_format}",
    ]

    if strategy.constraints:
        sections.append(
            "Constraints:\n" +
            "\n".join(
                f"- {c}" for c in strategy.constraints
            )
        )

    sections.append(
        f"User Request:\n{user_input}"
    )

    return "\n\n".join(sections)