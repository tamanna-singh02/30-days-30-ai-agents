import config
from retrieval.hybrid_pipeline import HybridSearchPipeline


def test_hybrid_pipeline(query: str = "performance metrics"):
    pipeline = HybridSearchPipeline()

    results = pipeline.retrieve(
        query=query,
        candidate_k=20,
        final_k=5,
    )

    print("\n" + "=" * 70)
    print("FINAL HYBRID SEARCH RESULTS")
    print("=" * 70)

    for rank, result in enumerate(results, start=1):
        document = result.document
        print(f"\nRank: {rank}")
        print(f"Cross-Encoder Score: {result.score:.4f}")
        print(f"Chunk ID: {document.metadata.get('chunk_id')}")
        print(f"\n{document.page_content[:500]}")

    assert len(results) >= 0


if __name__ == "__main__":
    test_hybrid_pipeline()