from rank_bm25 import BM25Okapi

class BM25Index:

    def __init__(self, documents):
        self.documents = documents

        tokenized_documents = [
            self._tokenize(doc.page_content)
            for doc in documents
        ]

        self.index = BM25Okapi(tokenized_documents)

    @staticmethod
    def _tokenize(text:str):
        return text.lower().split()

    def search(self, query:str, k: int = 20):
        tokenized_query = self._tokenize(query)
        scores = self.index.get_scores(tokenized_query)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:k]

        return[{
            "document": self.documents[i],
            "score":scores[i],
            "rank": rank + 1
        } for rank, i in enumerate(ranked_indices)]

    