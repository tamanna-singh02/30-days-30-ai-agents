"""
Prompt templates for the Map-Reduce Summarizer.
"""

MAP_PROMPT = """You are an expert technical writer.

Your task is to summarize the following section.

Requirements:
- Preserve all important facts.
- Keep names and numbers.
- Remove unnecessary details.
- Maximum 150 words.

Text:
{chunk}
"""

REDUCE_PROMPT = """You are combining summaries from multiple sections of the same document.

Requirements:
- Remove duplicated ideas.
- Preserve chronology.
- Keep technical terms.
- Produce one coherent summary.
- Maximum 400 words.

Summaries:
{summaries}
"""
