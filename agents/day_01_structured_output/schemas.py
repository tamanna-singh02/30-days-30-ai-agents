from pydantic import BaseModel, Field
from typing import List, Optional

class CandidateProfile(BaseModel):
    """
    Strict schema for extracting candidate information from a resume.
    """
    
    full_name: str = Field(
        description="The candidate's full legal name"
    )
    
    years_experience: int = Field(
        description="Total years of professional experience"
    )

    primary_skills: List[str] = Field(
        description="List of 3 to 5 core technical skills"
    )

    highest_degree: Optional[str] = Field(
        description="Highest academic degree obtained (e.g., B.Tech, Masters)"
    )

    is_hireable: bool = Field(
        description="True if the candidate has at least 1 year of experience and technical skills"
    )