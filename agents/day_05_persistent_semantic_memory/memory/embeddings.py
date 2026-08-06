
from langchain_core.embeddings import Embeddings
from shared.config import OPENAI_API_KEY

def _get_embeddings():
    if OPENAI_API_KEY and OPENAI_API_KEY != "your_openai_api_key_here":
        try:
            from langchain_openai import OpenAIEmbeddings
            from config import EMBEDDING_MODEL
            emb = OpenAIEmbeddings(model=EMBEDDING_MODEL, api_key=OPENAI_API_KEY)
            emb.embed_query("test")
            return emb
        except Exception:
            pass

    from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

    class ChromaEmbeddings(Embeddings):
        def __init__(self):
            self._fn = DefaultEmbeddingFunction()

        def embed_documents(self, texts: list[str]) -> list[list[float]]:
            return self._fn(texts)

        def embed_query(self, text: str) -> list[float]:
            return self._fn([text])[0]

    return ChromaEmbeddings()

embeddings = _get_embeddings()