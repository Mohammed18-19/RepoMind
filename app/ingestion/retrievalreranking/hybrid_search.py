from app.ingestion.retrievalreranking.semantic_search import SemanticSearch
from app.ingestion.retrievalreranking.keyword_search import KeywordSearch


class HybridSearch:
    RRF_K = 60

    SEMANTIC_TOP_K = 50
    KEYWORD_TOP_K = 50
    RRF_TOP_K = 30

    def __init__(self):
        self.semantic_search = SemanticSearch()
        self.keyword_search = KeywordSearch()

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

        for rank, (chunk, semantic_score) in enumerate(
            semantic_results,
            start=1,
        ):
            results[chunk.id] = {
                "chunk": chunk,
                "semantic_score": semantic_score,
                "keyword_score": 0.0,
                "semantic_rank": rank,
                "keyword_rank": None,
            }

        for rank, (chunk, keyword_score) in enumerate(
            keyword_results,
            start=1,
        ):
            if chunk.id not in results:
                results[chunk.id] = {
                    "chunk": chunk,
                    "semantic_score": 0.0,
                    "keyword_score": keyword_score,
                    "semantic_rank": None,
                    "keyword_rank": rank,
                }
            else:
                results[chunk.id]["keyword_score"] = keyword_score
                results[chunk.id]["keyword_rank"] = rank

        for result in results.values():
            rrf_score = 0.0

            if result["semantic_rank"] is not None:
                rrf_score += 1 / (
                    self.RRF_K
                    + result["semantic_rank"]
                )

            if result["keyword_rank"] is not None:
                rrf_score += 1 / (
                    self.RRF_K
                    + result["keyword_rank"]
                )

            result["hybrid_score"] = rrf_score

        ranked_results = sorted(
            results.values(),
            key=lambda result: result["hybrid_score"],
            reverse=True,
        )

        return ranked_results[:top_k]
