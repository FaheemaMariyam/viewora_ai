#Orchestrates retrieval + analytics + LLM generation using LangChain
from app.rag.generator import generate_ai_answer


def run_rag_chain(docs, analytics: str, question: str) -> str:
    context = "\n\n".join(doc.page_content for doc in docs)
    return generate_ai_answer(context, analytics, question)

