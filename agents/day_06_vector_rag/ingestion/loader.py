from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document


class DocumentLoader:
    """
    Responsible for loading documents from disk.

    Supports PDF (.pdf), Markdown (.md), and Text (.txt) files.
    """

    def load_document(self, file_path: str | Path) -> list[Document]:
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")

        ext = file_path.suffix.lower()

        if ext == ".pdf":
            loader = PyPDFLoader(str(file_path))
            documents = loader.load()
        elif ext in (".md", ".txt", ".markdown"):
            loader = TextLoader(str(file_path), encoding="utf-8")
            documents = loader.load()
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        for document in documents:
            document.metadata.update(
                {"source": file_path.name, "file_path": str(file_path)}
            )

        return documents

    def load_pdf(self, file_path: str | Path) -> list[Document]:
        return self.load_document(file_path)


def load_document(file_path: str | Path) -> list[Document]:
    """
    Convenience function for loading documents.
    """
    loader = DocumentLoader()
    return loader.load_document(file_path)