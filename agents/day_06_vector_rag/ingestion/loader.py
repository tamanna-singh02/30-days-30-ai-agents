from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


class DocumentLoader:
    """
    Responsible for loading documents from disk.

    Currently supports PDF files.
    """

    def load_pdf(self, file_path: str | Path) -> list[Document]:
        """
        Load a PDF and return LangChain Document objects.
        """

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")

        if file_path.suffix.lower() != ".pdf":
            raise ValueError(f"Unsupported file type: {file_path.suffix}")

        loader = PyPDFLoader(str(file_path))
        documents = loader.load()

        # Add useful metadata
        for document in documents:
            document.metadata.update(
                {"source": file_path.name, "file_path": str(file_path)}
            )

        return documents


def load_document(file_path: str | Path) -> list[Document]:
    """
    Convenience function for loading a documents.
    """

    loader = DocumentLoader()
    return loader.load_pdf(file_path)


    