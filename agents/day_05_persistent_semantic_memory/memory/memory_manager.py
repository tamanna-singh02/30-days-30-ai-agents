from typing import List

from memory.schemas import Memory
from memory.kv_store import kv_store
from memory.vector_store import vector_store


class MemoryManager:
    """
    Coordinates all memory operations.

    Responsibilities
    ----------------
    • Route structured memories to KV Store
    • Route semantic memories to Vector Store
    • Retrieve memories
    • Keep future memory logic in one place
    """

    # -------------------------
    # SAVE
    # -------------------------

    def save(self, memory: Memory) -> None:

        if memory.key:
            kv_store.save(memory)

        vector_store.save(memory)

    def save_many(
        self,
        memories: List[Memory],
    ):

        for memory in memories:
            self.save(memory)

    # -------------------------
    # RETRIEVAL
    # -------------------------

    def retrieve(
        self,
        query: str,
        k: int = 5,
    ):

        return vector_store.search(
            query=query,
            k=k,
        )

    def retrieve_category(
        self,
        query: str,
        category: str,
        k: int = 5,
    ):

        return vector_store.search_by_category(
            query=query,
            category=category,
            k=k,
        )

    # -------------------------
    # FACT LOOKUP
    # -------------------------

    def get_fact(
        self,
        key: str,
    ):

        return kv_store.get(key)

    # -------------------------
    # UPDATE
    # -------------------------

    def update(
        self,
        memory: Memory,
    ):

        if memory.key:
            kv_store.save(memory)

        vector_store.update(memory)

    # -------------------------
    # DELETE
    # -------------------------

    def delete(
        self,
        memory: Memory,
    ):

        if memory.key:
            kv_store.delete(memory.key)

        vector_store.delete(memory.id)

    # -------------------------
    # DEBUG
    # -------------------------

    def list_all_facts(self):

        return kv_store.list_all()

    def count_vector_memories(self):

        return vector_store.count()


memory_manager = MemoryManager()
