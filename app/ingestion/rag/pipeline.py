from app.ingestion.retrievalreranking.hybrid_search import HybridSearch
from app.ingestion.retrievalreranking.reranker import Reranker
from app.ingestion.rag.context_builder import ContextBuilder
from app.ingestion.rag.generator import RAGGenerator


class RAGPipeline:
    def __init__(self):
        self.hybrid_search = HybridSearch()
        self.reranker = Reranker()
        self.context_builder = ContextBuilder()
        self.generator = RAGGenerator()

    def answer(
        self,
        question: str,
        retrieval_top_k: int = 10,
        final_top_k: int = 5,
    ) -> str:
        candidates = self.hybrid_search.search(
            query=question,
            top_k=retrieval_top_k,
        )

        ranked_results = self.reranker.rerank(
            query=question,
            candidates=candidates,
            top_k=final_top_k,
        )

        context = self.context_builder.build(
            ranked_results
        )

        answer = self.generator.generate(
            question=question,
            context=context,
        )

        return answer