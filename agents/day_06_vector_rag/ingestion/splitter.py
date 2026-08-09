from langchain_core.documents import Document
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    TokenTextSplitter,
)

from config import settings


class ChunkingService:
    """
    Handles document chunking using different strategies.

    Supported strategies:
    - recursive
    - character
    - token
    """

    def __init__(
        self,
        strategy: str = "recursive",
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ):
        self.strategy = strategy
        self.chunk_size = (
            chunk_size if chunk_size is not None else settings.CHUNK_SIZE
        )
        self.chunk_overlap = (
            chunk_overlap if chunk_overlap is not None else settings.CHUNK_OVERLAP
        )

        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("Chunk overlap must be smaller than chunk size")

        self.splitter = self._create_splitter()

    def _create_splitter(self):
        """
        Create the appropriate text splitter.
        """
        if self.strategy == "recursive":
            return RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                separators=[
                    "\n\n",
                    "\n",
                    ". ",
                    "! ",
                    "? ",
                    " ",
                    "",
                ],
            )

        if self.strategy == "character":
            return CharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                separator="\n",
            )

        if self.strategy == "token":
            return TokenTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
            )

        raise ValueError(f"Unsupported chunking strategy: {self.strategy}")

    def split_documents(self, documents: list[Document]) -> list[Document]:
        """
        Split documents into smaller chunks.
        """
        chunks = self.splitter.split_documents(documents)

        # Add chunk index for traceability
        for index, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = index
            chunk.metadata["chunk_size"] = len(chunk.page_content)

        return chunks

    def get_statistics(self, chunks: list[Document]) -> dict:
        """Return basic statistics about generated chunks."""
        if not chunks:
            return {
                "total_chunks": 0,
                "average_length": 0,
                "min_length": 0,
                "max_length": 0,
            }

        lengths = [len(chunk.page_content) for chunk in chunks]

        return {
            "total_chunks": len(chunks),
            "average_length": round(sum(lengths) / len(lengths), 2),
            "min_length": min(lengths),
            "max_length": max(lengths),
        }


# Alias for compatibility
Chunker = ChunkingService