import os

from dotenv import load_dotenv
from google import genai

from app.ingestion.rag.prompts import RAGPrompt


load_dotenv()


class RAGGenerator:
    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )
        self.prompt_builder = RAGPrompt()

    def generate(self, question: str, context: str) -> str:
        prompt = self.prompt_builder.build(
            question=question,
            context=context,
        )

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text