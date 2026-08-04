from pydantic import BaseModel, Field

class UserMemory(BaseModel):
    name: str | None = None
    professional: str | None = None
    company: str | None = None
    city: str | None = None

    hobbies: list[str] = Field(default_factory=list)
    preferences: list[str] = Field(default_factory=list)