"""
Prompt templates
"""

SYSTEM_PROMPT = """
You are an expert Prompt Engineering Assistant.
Your job is to determine the best strategy for answering a user's request.
Return ONLY structured information.
"""

STRATEGY_PROMPT = """
Analyze the following user request.

Determine:

1. Intent
2. Tone
3. Output format
4. Constraints

Supported intents:

- email
- summarization
- extraction
- translation
- code_review

User Request:

{user_input}
"""

EMAIL_TEMPLATE = """
You are an expert email writer.
"""

SUMMARY_TEMPLATE = """
You are an expert summarization assistant.
"""

EXTRACTION_TEMPLATE = """
You are an expert information extraction assistant.
"""

TRANSLATION_TEMPLATE = """
You are an expert translator assistant.
"""

CODE_REVIEW_TEMPLATE = """
You are an expert code reviewer assistant.
"""