import re
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi


class BM25Index:

    def __init__(self, documents: list[Document]):
        self.documents = documents
        if documents:
            tokenized_documents = [
                self._tokenize(document.page_content)
                for document in documents
            ]
            self.bm25 = BM25Okapi(tokenized_documents)
        else:
            self.bm25 = None

    @staticmethod
    def _tokenize(text: str):
        return re.findall(
            r"[a-zA-Z0-9_]+",
            text.lower(),
        )

    def search(self, query: str, k: int = 20):
        if not self.documents or not self.bm25:
            return []

        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True,
        )[:k]

        results = []

        for rank, index in enumerate(
            ranked_indices,
            start=1,
        ):
            results.append(
                {
                    "document": self.documents[index],
                    "score": float(scores[index]),
                    "rank": rank,
                }
            )

        return results