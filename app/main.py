from fastapi import FastAPI

from app.rag.documents import property_to_document
from app.rag.embeddings import get_embeddings
from app.rag.vector_store import create_vector_store
from app.api.v1.area_insights import router as area_router

app = FastAPI(title="Viewora AI Service")


@app.on_event("startup")
def startup_event():
    """
    Initialize RAG state ONCE at startup
    """
    # TEMP data (replace later with DB fetch)
    properties = [
        {
            "id": 1,
            "type": "Flat",
            "city": "Kochi",
            "locality": "Kakkanad",
            "price_range": "70-80 Lakhs",
            "area_size": "1450 sqft",
            "amenities": ["Parking", "Lift"],
        }
    ]

    documents = [property_to_document(p) for p in properties]

    embeddings = get_embeddings()

    vector_store = create_vector_store(documents, embeddings)

    # ✅ STORE IN APP STATE (CRITICAL)
    app.state.vector_store = vector_store


@app.get("/health")
def health():
    return {"status": "AI service running"}


# Register routes
app.include_router(area_router, prefix="/ai")
