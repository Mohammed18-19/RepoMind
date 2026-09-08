from sentence_transformers import CrossEncoder


class Reranker:
    def __init__(self):
        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
        self,
        query: str,
        candidates: list[dict],
        top_k: int = 5,
    ) -> list[dict]:

        pairs = [
            (query, candidate["chunk"].content)
            for candidate in candidates
        ]

        scores = self.model.predict(pairs)

        for candidate, score in zip(candidates, scores):
            candidate["rerank_score"] = float(score)

        ranked_results = sorted(
            candidates,
            key=lambda candidate: candidate["rerank_score"],
            reverse=True,
        )

        return ranked_results[:top_k]