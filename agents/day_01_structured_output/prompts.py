"""
Prompt templates used by the Structured Data Extractor Agent.
Keeping prompts in a separate module makes them easier to maintain
and experiment with without modifying the workflow logic.
"""

SYSTEM_PROMPT = """
You are an expert information extraction system.

Extract structured candidate information from resumes.

Rules:
1. Return only the requested information.
2. Do not hallucinate missing information.
3. Extract only skills directly mentioned in the resume text. Do not invent or extrapolate skills.
4. years_experience must always be an integer.
"""

def build_extraction_prompt(resume_text: str) -> str:
    """
    Creates the extraction prompt sent to the LLM.
    """
    return f"""
    Extract the candidate profile from the resume below.

    Resume:
    
    {resume_text}
    """

def build_retry_prompt(
    resume_text: str,
    validation_error: str,
) -> str:
    """
    Prompt used after validation fails.
    """
    return f"""
    Your previous response failed validation.

    Validation Error:

    {validation_error}

    Please correct the response.

    Resume:

    {resume_text}
    """