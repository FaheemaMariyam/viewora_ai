import os
import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Import components
from app.rag.documents import property_to_document
from app.rag.embeddings import get_embeddings
from app.rag.vector_store import create_vector_store
from app.api.v1.area_insights import router as area_router

# Force load environment
load_dotenv()

app = FastAPI(title="Viewora AI Service")

# This will hold our vector store
app.state.vector_store = None

@app.on_event("startup")
def startup_event():
    """
    Final Fix: Connects directly to Postgres. 
    NO MORE calls to /api/properties/ai-rag/
    """
    print("🚀 AI SERVICE STARTING: Using DIRECT POSTGRES connection (Fix v3)")
    
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "viewora_db"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "root"),
            host=os.getenv("DB_HOST", "postgres"),
            port=os.getenv("DB_PORT", "5432"),
            cursor_factory=RealDictCursor
        )
        cur = conn.cursor()
        
        # Load real data
        query = """
            SELECT id, property_type as type, city, locality, price, 
                   area_size, area_unit, bedrooms, bathrooms, description
            FROM properties_property 
            WHERE status = 'published' AND is_active = true
        """
        cur.execute(query)
        rows = cur.fetchall()
        
        properties = []
        for row in rows:
            properties.append({
                "id": row['id'],
                "type": row['type'],
                "city": row['city'],
                "locality": row['locality'],
                "price_range": f"{row['price']} INR",
                "area_size": f"{row['area_size']} {row['area_unit']}",
                "amenities": [f"{row['bedrooms']} BHK"] if row['bedrooms'] else []
            })
            
        cur.close()
        conn.close()
        print(f"✅ Success: Found {len(properties)} properties in Database.")

        if properties:
            print("🧠 Building Vector Search Index...")
            docs = [property_to_document(p) for p in properties]
            embeddings = get_embeddings()
            app.state.vector_store = create_vector_store(docs, embeddings)
            print("🎯 Vector Index is READY.")
        else:
            print("⚠️ No properties found. AI context will be empty.")

    except Exception as e:
        print(f"❌ DATABASE ERROR: Could not connect or fetch properties: {e}")

@app.get("/health")
def health():
    return {"status": "up", "rag_ready": app.state.vector_store is not None}

# Register the AI route
app.include_router(area_router, prefix="/ai")
