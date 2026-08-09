from langchain_huggingface import HuggingFaceEmbeddings
from config import settings


class EmbeddingService:
    """
    Creates dense vector embeddings for documents and queries.
    """

    def __init__(self, model_name: str | None = None):
        configured_model = model_name or settings.EMBEDDING_MODEL
        if "text-embedding" in str(configured_model).lower():
            self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
        else:
            self.model_name = configured_model

        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={
                "device": "cpu",
            },
            encode_kwargs={"normalize_embeddings": True},
        )

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for a list of text documents.
        """
        return self.embeddings.embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        """
        Generate an embedding for a single query.
        """
        return self.embeddings.embed_query(text)

    def get_embedding_model(self):
        """
        Return the underlying LangChain embedding object.
        """
        return self.embeddings


embedder = EmbeddingService()