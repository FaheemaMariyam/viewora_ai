from fastapi import APIRouter, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from app.rag.retriever import get_retriever
from app.rag.chain import run_rag_chain
from app.analytics.dynamo import get_property_analytics

router = APIRouter()


class AreaInsightRequest(BaseModel):
    question: str


@router.post("/area-insights")
def area_insights(request: Request, payload: AreaInsightRequest):
    # ✅ READ FROM FASTAPI APP STATE
    vector_store = getattr(request.app.state, "vector_store", None)

    if vector_store is None:
        return JSONResponse(
            status_code=503,
            content={"error": "RAG vector store not initialized"},
        )

    retriever = get_retriever(vector_store)
    docs = retriever.invoke(payload.question)

    property_ids = [
        doc.metadata.get("property_id")
        for doc in docs
        if doc.metadata
    ]

    analytics = get_property_analytics(property_ids)

    answer = run_rag_chain(docs, analytics, payload.question)

    return {
        "answer": answer,
        "sources": [doc.metadata for doc in docs],
    }
