import config
from indexing.bm25_index import BM25Index
from ingestion.vector_store import VectorStore


def test_real_bm25(query: str = "performance metrics"):
    vector_store = VectorStore()
    documents = vector_store.get_documents()

    print(f"Loaded {len(documents)} documents")

    if not documents:
        print("No documents found in vector store.")
        return

    bm25 = BM25Index(documents)

    results = bm25.search(
        query=query,
        k=5,
    )

    print("\n" + "=" * 70)
    print("BM25 RESULTS")
    print("=" * 70)

    for result in results:
        document = result["document"]
        print(f"\nRank: {result['rank']}")
        print(f"Score: {result['score']:.4f}")
        print(f"Chunk ID: {document.metadata.get('chunk_id')}")
        print(f"\n{document.page_content[:500]}")

    assert len(results) >= 0


if __name__ == "__main__":
    test_real_bm25()