EVALUATION_DATASET = [
    {
        "query": "What are the three real problems created when an LLM takes a closed-book exam?",
        "query_type": "Semantic Search",
        "ground_truth": "1. Knowledge cutoff\n2. No access to private/internal data\n3. Hallucination",
        "key_phrases": ["knowledge cutoff", "private", "hallucination"],
    },
    {
        "query": "What is RAGAS and what does it evaluate?",
        "query_type": "Exact Keyword (Lexical)",
        "ground_truth": "RAGAS is an evaluation framework for RAG systems assessing faithfulness, answer relevance, context recall, and context precision.",
        "key_phrases": ["ragas", "faithfulness", "context recall", "precision"],
    },
    {
        "query": "How does Reciprocal Rank Fusion (RRF) calculate candidate document scores?",
        "query_type": "Technical Concept",
        "ground_truth": "RRF calculates scores by summing 1 / (k + rank) for each candidate across multiple retrieval rank lists.",
        "key_phrases": ["1 / (k + rank)", "rank", "summing"],
    },
    {
        "query": "What performance metrics and daily tracking items are recorded in the report?",
        "query_type": "Multi-document Query",
        "ground_truth": "Weight, gym performance, hunger, recovery, calories, and protein intake.",
        "key_phrases": ["weight", "gym", "calories", "protein"],
    },
    {
        "query": "What environment variable configures the Redis cluster connection string REDIS_URL?",
        "query_type": "Exact Token (Code/Config)",
        "ground_truth": "REDIS_URL=redis://:secret_pass@cache.internal.domain:6379/0",
        "key_phrases": ["REDIS_URL", "secret_pass", "6379"],
    },
    {
        "query": "What secret key JWT_SECRET is used for signing access tokens?",
        "query_type": "Exact Token (Code/Config)",
        "ground_truth": "JWT_SECRET=super_secret_jwt_token_key_2026_prod",
        "key_phrases": ["JWT_SECRET", "super_secret_jwt_token_key_2026_prod"],
    },
    {
        "query": "When does the API gateway return a 401 Unauthorized error response?",
        "query_type": "Exact Token (Error Code)",
        "ground_truth": "401 Unauthorized is returned when a request lacks a valid Bearer token or when JWT_SECRET verification fails.",
        "key_phrases": ["401 Unauthorized", "Bearer token", "JWT_SECRET"],
    },
    {
        "query": "What is the endpoint /api/v1/auth/token used for?",
        "query_type": "Exact Token (API Route)",
        "ground_truth": "POST /api/v1/auth/token exchanges client API credentials for an authenticated short-lived JWT access token.",
        "key_phrases": ["/api/v1/auth/token", "access token"],
    },
]


