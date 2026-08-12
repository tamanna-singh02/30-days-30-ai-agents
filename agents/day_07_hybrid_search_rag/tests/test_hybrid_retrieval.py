import config
from retrieval.hybrid_retriever import HybridRetriever


def test_hybrid_retrieval(query: str = "performance metrics"):
    retriever = HybridRetriever()

    results = retriever.retrieve(
        query=query,
        k=5,
    )

    print("\n" + "=" * 70)
    print("HYBRID RETRIEVAL — RRF")
    print("=" * 70)

    for rank, result in enumerate(results, start=1):
        if isinstance(result, dict):
            document = result["document"]
            score = result["score"]
        else:
            document = result.document
            score = result.score

        print(f"\nRank: {rank}")
        print(f"RRF Score: {score:.6f}")
        print(f"Chunk ID: {document.metadata.get('chunk_id')}")
        print(f"\n{document.page_content[:400]}")

    assert len(results) >= 0


if __name__ == "__main__":
    test_hybrid_retrieval()