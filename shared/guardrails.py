"""
Guardrails and validation helpers for input/output sanitization.
"""

def sanitize_input_text(text: str) -> str:
    """
    Strips leading/trailing whitespaces and basic control characters.
    """
    if not text:
        return ""
    return text.strip()

def validate_response_non_empty(response: str) -> bool:
    """
    Ensures response text is not empty or whitespace only.
    """
    return bool(response and response.strip())
