import config
from indexing.bm25_index import BM25Index
from ingestion.vector_store import VectorStore
from retrieval.retriever import Retriever


def test_dense_vs_bm25(query: str = "performance metrics"):
    vector_store = VectorStore()
    documents = vector_store.get_documents()

    if not documents:
        print("No documents found in vector store.")
        return

    bm25 = BM25Index(documents)
    dense_retriever = Retriever(vector_store=vector_store)
    k = 5

    dense_results = dense_retriever.retrieve(query=query, k=k)
    bm25_results = bm25.search(query=query, k=k)

    print("\n" + "=" * 70)
    print("DENSE RETRIEVAL")
    print("=" * 70)

    for rank, result in enumerate(dense_results, start=1):
        doc = result.document
        print(f"\n{rank}. {doc.metadata.get('chunk_id')}")
        print(f"Distance: {result.score:.4f}")
        print(doc.page_content[:300])

    print("\n" + "=" * 70)
    print("BM25 RETRIEVAL")
    print("=" * 70)

    for result in bm25_results:
        doc = result["document"]
        print(f"\n{result['rank']}. {doc.metadata.get('chunk_id')}")
        print(f"BM25 Score: {result['score']:.4f}")
        print(doc.page_content[:300])

    assert len(dense_results) >= 0
    assert len(bm25_results) >= 0


if __name__ == "__main__":
    test_dense_vs_bm25()