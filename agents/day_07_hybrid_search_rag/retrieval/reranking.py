from dataclasses import dataclass

from langchain_core.documents import Document


@dataclass
class RerankedDocument:
    """
    Document returned after Cross-Encoder reranking.
    """

    document: Document
    score: float