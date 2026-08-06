import hashlib
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

MemoryCategory = Literal[
    "identity",
    "professional",
    "preference",
    "goal",
    "project",
    "experience",
    "skill",
    "custom"
]

class Memory(BaseModel):
    id: str | None = None
    category: MemoryCategory
    key: str | None = None
    value: str
    source: str = "conversation"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def model_post_init(self, __context):
        if not self.id:
            if self.key and self.key.strip():
                norm_key = self.key.strip().lower().replace(" ", "_")
                self.id = f"{self.category}:{norm_key}"
            else:
                norm_val = self.value.strip().lower()
                hash_digest = hashlib.md5(norm_val.encode("utf-8")).hexdigest()[:12]
                self.id = f"{self.category}:{hash_digest}"
    