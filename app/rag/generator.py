
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

def generate_ai_answer(context: str, analytics: str, question: str) -> str:
    prompt = f"""
You are an AI real-estate advisor.

Context (similar properties):
{context}

Analytics (user behavior signals):
{analytics}

User Question:
{question}

Rules:
- Do NOT guarantee profits
- Use cautious language
- Explain reasoning clearly
- Mention risks
"""

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt
    )

    return response.text.strip() if response.text else "No response generated."
