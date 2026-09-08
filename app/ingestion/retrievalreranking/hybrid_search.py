from app.ingestion.retrievalreranking.semantic_search import SemanticSearch
from app.ingestion.retrievalreranking.keyword_search import KeywordSearch


class HybridSearch:
    def __init__(self):
        self.semantic_search = SemanticSearch()
        self.keyword_search = KeywordSearch()

    def search(self, query: str, top_k: int = 5):
        semantic_results = self.semantic_search.search(
            query,
            top_k=top_k,
        )

        keyword_results = self.keyword_search.search(
            query,
            top_k=top_k,
        )

        results = {}

        # Add semantic results
        for chunk, semantic_score in semantic_results:
            results[chunk.id] = {
                "chunk": chunk,
                "semantic_score": semantic_score,
                "keyword_score": 0.0,
            }

        # Add keyword results
        for chunk, keyword_score in keyword_results:
            if chunk.id in results:
                results[chunk.id]["keyword_score"] = keyword_score
            else:
                results[chunk.id] = {
                    "chunk": chunk,
                    "semantic_score": 0.0,
                    "keyword_score": keyword_score,
                }

        # Calculate hybrid score
        for result in results.values():
            result["hybrid_score"] = (
                0.7 * result["semantic_score"]
                + 0.3 * result["keyword_score"]
            )

        # Sort by hybrid score: highest first
        ranked_results = sorted(
            results.values(),
            key=lambda result: result["hybrid_score"],
            reverse=True,
        )

        return ranked_results[:top_k]