from typing import List
from langchain_chroma import Chroma
from langchain_core.documents import Document

from config import CHROMA_DIR
from memory.embeddings import embeddings
from memory.schemas import Memory


class VectorStore:
    def __init__(self):
        self.collection = Chroma(
            collection_name="semantic_memory",
            persist_directory=str(CHROMA_DIR),
            embedding_function=embeddings,
        )

    def save(self, memory: Memory) -> None:
        content = f"{memory.key}: {memory.value}" if memory.key else memory.value
        doc = Document(
            page_content=content,
            metadata={
                "id": memory.id,
                "category": memory.category,
                "key": memory.key or "",
                "source": memory.source,
            },
        )
        try:
            self.collection.delete(ids=[memory.id])
        except Exception:
            pass
        self.collection.add_documents(documents=[doc], ids=[memory.id])

    def search(self, query: str, k: int = 5) -> List[Document]:
        return self.collection.similarity_search(query=query, k=k)

    def search_by_category(self, query: str, category: str, k: int = 5) -> List[Document]:
        return self.collection.similarity_search(query=query, k=k, filter={"category": category})

    def update(self, memory: Memory) -> None:
        self.delete(memory.id)
        self.save(memory)

    def delete(self, memory_id: str) -> None:
        self.collection.delete(ids=[memory_id])

    def count(self) -> int:
        return len(self.collection.get()["ids"])


vector_store = VectorStore()



