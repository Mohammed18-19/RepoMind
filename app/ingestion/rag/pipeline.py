from app.ingestion.retrievalreranking.hybrid_search import HybridSearch
from app.ingestion.retrievalreranking.reranker import Reranker
from app.ingestion.rag.context_builder import ContextBuilder
from app.ingestion.rag.generator import RAGGenerator
from app.ingestion.rag.conversation_manager import ConversationManager


class RAGPipeline:
    def __init__(self):
        self.hybrid_search = HybridSearch()
        self.reranker = Reranker()
        self.context_builder = ContextBuilder()
        self.generator = RAGGenerator()

    def _format_history(self, messages) -> str:
        if not messages:
            return ""

        lines = []

        for message in messages:
            role = message.role.upper()
            lines.append(f"{role}: {message.content}")

        return "\n".join(lines)

    def answer(
        self,
        question: str,
        retrieval_top_k: int = 10,
        final_top_k: int = 5,
        conversation_id: int | None = None,
    ) -> str:

        conversation_manager = None

        try:
            history = ""

            if conversation_id is not None:
                conversation_manager = ConversationManager()

                conversation = conversation_manager.get_conversation(
                    conversation_id
                )

                if conversation is None:
                    raise ValueError(
                        f"Conversation {conversation_id} does not exist."
                    )

                messages = conversation_manager.get_history(
                    conversation_id
                )

                history = self._format_history(messages)

                conversation_manager.save_message(
                    conversation_id=conversation_id,
                    role="user",
                    content=question,
                )

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
                history=history,
            )

            if conversation_manager is not None:
                conversation_manager.save_message(
                    conversation_id=conversation_id,
                    role="assistant",
                    content=answer,
                )

            return answer

        finally:
            if conversation_manager is not None:
                conversation_manager.close()
