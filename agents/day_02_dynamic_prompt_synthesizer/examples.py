"""
Few shot examples.
"""

EMAIL_EXAMPLES = [
    {
        "input": "Write a resignation email.",
        "output": "Professional resignation email...",
    }
]

SUMMARY_EXAMPLES = [
    {
        "input": "Summarize this meeting...",
        "output": "Key Decisions\nAction Items"
    }
]

EXTRACTION_EXAMPLES = [
    {
        "input": "Invoice #123...",
        "output": '{"invoice": "123"}'
    }
]