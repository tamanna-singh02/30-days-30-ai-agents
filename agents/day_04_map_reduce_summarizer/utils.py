"""
Utility functions for document processing and statistics calculation.
"""

import os
import tiktoken
from shared.logger import logger
from .config import CHUNK_SIZE, CHUNK_OVERLAP


def load_document(file_path: str) -> str:
    """
    Load a text or PDF document from disk.
    Supports .txt and .pdf files (using available PDF readers like PyMuPDF, pypdf, PyPDF2, pdfplumber).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        logger.info(f"Detected PDF file: {file_path}. Extracting text...")
        text = ""

        # Try PyMuPDF (fitz)
        try:
            import fitz
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text() + "\n"
            doc.close()
            return text
        except ImportError:
            pass

        # Try pypdf
        try:
            import pypdf
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                text += (page.extract_text() or "") + "\n"
            return text
        except ImportError:
            pass

        # Try PyPDF2
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(file_path)
            for page in reader.pages:
                text += (page.extract_text() or "") + "\n"
            return text
        except ImportError:
            pass

        # Try pdfplumber
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += (page.extract_text() or "") + "\n"
            return text
        except ImportError:
            pass

        raise ImportError(
            "No PDF parser library (PyMuPDF/fitz, pypdf, PyPDF2, pdfplumber) is installed."
        )

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def get_encoding():
    """
    Return the tokenizer encoding.
    """
    return tiktoken.encoding_for_model("gpt-4o-mini")


def count_tokens(text: str) -> int:
    """
    Count the number of tokens in a text.
    """
    encoding = get_encoding()
    return len(encoding.encode(text))


def split_into_chunks(text: str) -> list[str]:
    """
    Split text into overlapping token-based chunks.
    """
    encoding = get_encoding()
    tokens = encoding.encode(text)

    chunks = []
    start = 0

    while start < len(tokens):
        end = start + CHUNK_SIZE
        chunk_tokens = tokens[start:end]
        chunk = encoding.decode(chunk_tokens)
        chunks.append(chunk)
        start += CHUNK_SIZE - CHUNK_OVERLAP
        if end >= len(tokens):
            break

    return chunks


def calculate_chunk_stats(chunks: list[str]) -> dict:
    """
    Calculate token statistics across all document chunks.
    """
    if not chunks:
        return {
            "avg_tokens_per_chunk": 0.0,
            "largest_chunk": 0,
            "smallest_chunk": 0,
        }

    chunk_token_counts = [count_tokens(c) for c in chunks]
    avg_tokens = round(sum(chunk_token_counts) / len(chunks), 2)
    largest = max(chunk_token_counts)
    smallest = min(chunk_token_counts)

    return {
        "avg_tokens_per_chunk": avg_tokens,
        "largest_chunk": largest,
        "smallest_chunk": smallest,
    }