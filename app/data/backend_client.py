import os
import requests

BACKEND_API_URL = os.getenv(
    "BACKEND_API_URL", "http://viewora_backend:8000"
)

def fetch_properties_for_rag():
    """
    Fetch properties from Django backend for RAG indexing
    """
    try:
        response = requests.get(
            f"{BACKEND_API_URL}/api/properties/ai-rag/",
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Failed to fetch properties for RAG:", e)
        return []
