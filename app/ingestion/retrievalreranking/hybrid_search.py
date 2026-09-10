from app.ingestion.retrievalreranking.semantic_search import SemanticSearch
from app.ingestion.retrievalreranking.keyword_search import KeywordSearch


class HybridSearch:
    SEMANTIC_TOP_K = 50
    KEYWORD_TOP_K = 50

    SEMANTIC_WEIGHT = 0.7
    KEYWORD_WEIGHT = 0.3

    def __init__(self):
        self.semantic_search = SemanticSearch()
        self.keyword_search = KeywordSearch()

    @staticmethod
    def _normalize_scores(results: dict, score_key: str) -> None:
        scores = [
            result[score_key]
            for result in results.values()
            if result[score_key] is not None
        ]

        if not scores:
            return

        min_score = min(scores)
        max_score = max(scores)

        if max_score == min_score:
            for result in results.values():
                if result[score_key] is not None:
                    result[f"normalized_{score_key}"] = 1.0
            return

        for result in results.values():
            score = result[score_key]

            if score is None:
                result[f"normalized_{score_key}"] = 0.0
            else:
                result[f"normalized_{score_key}"] = (
                    (score - min_score)
                    / (max_score - min_score)
                )

    def search(
        self,
        query: str,
        top_k: int = 30,
        repository_id: int | None = None,
    ) -> list[dict]:

        semantic_results = self.semantic_search.search(
            query=query,
            top_k=self.SEMANTIC_TOP_K,
            repository_id=repository_id,
        )

        keyword_results = self.keyword_search.search(
            query=query,
            top_k=self.KEYWORD_TOP_K,
            repository_id=repository_id,
        )

        results = {}

        for chunk, score in semantic_results:
            results[chunk.id] = {
                "chunk": chunk,
                "semantic_score": score,
                "keyword_score": None,
            }

        for chunk, score in keyword_results:
            if chunk.id not in results:
                results[chunk.id] = {
                    "chunk": chunk,
                    "semantic_score": None,
                    "keyword_score": score,
                }
            else:
                results[chunk.id]["keyword_score"] = score

        self._normalize_scores(results, "semantic_score")
        self._normalize_scores(results, "keyword_score")

        for result in results.values():
            result["hybrid_score"] = (
                self.SEMANTIC_WEIGHT
                * result.get("normalized_semantic_score", 0.0)
                + self.KEYWORD_WEIGHT
                * result.get("normalized_keyword_score", 0.0)
            )

        ranked_results = sorted(
            results.values(),
            key=lambda result: result["hybrid_score"],
            reverse=True,
        )

        return ranked_results[:top_k]
