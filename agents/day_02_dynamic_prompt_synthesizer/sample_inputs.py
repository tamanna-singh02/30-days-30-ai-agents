"""
Sample user inputs for testing the Dynamic Prompt Synthesizer.
"""

EMAIL = """
Write a professional resignation email.

Maximum 150 words.

Thank my manager.
"""

SUMMARY = """
Summarize this meeting.

Use bullet points.

Mention action items.
"""

EXTRACTION = """
Extract

Invoice Number

Vendor

Amount

Date

from this invoice...
"""

TRANSLATION = """
Translate this paragraph from English to Spanish.

Keep the tone formal and respectful.
"""

CODE_REVIEW = """
Review this Python code snippet for potential security vulnerabilities and performance improvements.
"""

SAMPLE_INPUTS = [
    {
        "name": "Resignation Email",
        "input": EMAIL.strip()
    },
    {
        "name": "Meeting Notes Summarization",
        "input": SUMMARY.strip()
    },
    {
        "name": "Invoice Data Extraction",
        "input": EXTRACTION.strip()
    },
    {
        "name": "Translation",
        "input": TRANSLATION.strip()
    },
    {
        "name": "Code Review",
        "input": CODE_REVIEW.strip()
    }
]
