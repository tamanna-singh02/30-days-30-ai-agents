import sys
from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent.parent
DAY06_DIR = BASE_DIR.parent / "day_06_vector_rag"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(DAY06_DIR) not in sys.path:
    sys.path.insert(0, str(DAY06_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Chunking
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100

    # Retrieval
    TOP_K: int = 5
    RETRIEVAL_K: int = 20
    SIMILARITY_THRESHOLD: float = 1.5

    # Reranking
    ENABLE_RERANKING: bool = True
    RERANKER_MODEL: str = "cross-encoder/ms-marco-MiniLM-L6-v2"

    DOCUMENTS_DIR: Path = DAY06_DIR / "documents"
    VECTOR_DB_DIR: Path = DAY06_DIR / "database" / "chroma_db"

    model_config = SettingsConfigDict(
        env_file=(
            BASE_DIR / ".env",
            BASE_DIR.parent / ".env",
            BASE_DIR.parent.parent / ".env",
        ),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()

settings.DOCUMENTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

settings.VECTOR_DB_DIR.mkdir(
    parents=True,
    exist_ok=True,
)
