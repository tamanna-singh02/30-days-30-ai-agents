import config
from ingestion.vector_store import VectorStore


def test_chroma_documents():
    vector_store = VectorStore()
    documents = vector_store.get_documents()

    print(f"Total documents: {len(documents)}")

    for document in documents[:5]:
        print("\n" + "=" * 60)
        print("Chunk ID:", document.metadata.get("chunk_id"))
        print("Source:", document.metadata.get("source"))
        print("Page:", document.metadata.get("page"))
        print("Content:", document.page_content[:300])

    assert isinstance(documents, list)


if __name__ == "__main__":
    test_chroma_documents()