"""SQL query generator using LLM."""

import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


SYSTEM_PROMPT = """
You are a PostgreSQL SQL generation engine.

Your job is to convert a user's natural language question
into a SQL query using ONLY the provided database schema.

Rules:

1. Generate PostgreSQL SQL.
2. Only generate SELECT queries.
3. Never generate INSERT, UPDATE, DELETE, DROP, ALTER,
   TRUNCATE, CREATE, GRANT, REVOKE, or other mutating statements.
4. Use only tables and columns present in the schema.
5. Never invent tables or columns.
6. Always include a LIMIT clause.
7. Default LIMIT to 100 unless the user explicitly requests
   a smaller limit.
8. Never use SELECT *.
9. Prefer explicit column names.
10. Use table aliases when joins are required.
11. Use the relationships provided by the schema when joining tables.
12. Return ONLY the raw SQL query.
"""

def generate_sql(user_query: str, schema: str, feedback: str = None) -> str:

    prompt = f"""
    DATABASE SCHEMA:

    {schema}

    USER QUESTION:

    {user_query}
    """

    if feedback:
        prompt += f"""
    PREVIOUS VALIDATION ERROR:
    {feedback}

    Please fix the query to resolve the validation error while adhering strictly to all security rules.
    """

    prompt += "\n    Generate the safest valid PostgreSQL query that answers the question."

    if client:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        content = response.choices[0].message.content.strip()
    else:
        from shared.llm import get_llm
        from langchain_core.messages import SystemMessage, HumanMessage
        llm = get_llm(temperature=0.0)
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]
        response = llm.invoke(messages)
        content = response.content.strip()

    # Clean markdown code block formatting
    content = re.sub(r"^```sql\s*", "", content, flags=re.IGNORECASE)
    content = re.sub(r"^```\s*", "", content)
    content = re.sub(r"\s*```$", "", content)

    return content.strip()