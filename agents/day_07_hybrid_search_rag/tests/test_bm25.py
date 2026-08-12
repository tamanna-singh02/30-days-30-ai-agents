import config
from langchain_core.documents import Document

from indexing.bm25_index import BM25Index


def test_bm25():
    documents = [
        Document(
            page_content="Redis is used for distributed caching and session management.",
            metadata={"chunk_id": "chunk_001"},
        ),
        Document(
            page_content="PostgreSQL is the primary relational database used by the application.",
            metadata={"chunk_id": "chunk_002"},
        ),
        Document(
            page_content="The REDIS_URL environment variable contains the Redis connection string.",
            metadata={"chunk_id": "chunk_003"},
        ),
        Document(
            page_content="JWT authentication requires a valid access token.",
            metadata={"chunk_id": "chunk_004"},
        ),
    ]

    bm25 = BM25Index(documents)

    queries = [
        "Redis caching",
        "REDIS_URL",
        "JWT authentication",
        "relational database",
    ]

    for query in queries:
        print("\n" + "=" * 60)
        print(f"QUERY: {query}")
        print("=" * 60)

        results = bm25.search(
            query=query,
            k=2,
        )

        for result in results:
            print(
                f"{result['rank']}. score={result['score']:.4f} → {result['document'].page_content}"
            )

        assert len(results) > 0


if __name__ == "__main__":
    test_bm25()