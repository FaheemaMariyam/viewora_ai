#Converts property database records into AI-readable documents
from langchain_core.documents import Document

#This function converts one property from database into a format the AI can understand and search
def property_to_document(property_data: dict) -> Document:
    #This converts structured data into natural language text
    content = f"""
    Property Type: {property_data.get('type')}
    City: {property_data.get('city')}
    Locality: {property_data.get('locality')}
    Price Range: {property_data.get('price_range')}
    Area Size: {property_data.get('area_size')}
    Amenities: {', '.join(property_data.get('amenities', []))}
    """

    return Document(
        
        page_content=content.strip(),  #what the AI reads
        metadata={   #extra info for filtering & tracking
            "property_id": property_data.get("id"),
            "city": property_data.get("city"),
            "locality": property_data.get("locality"),
            "type": property_data.get("type"),
        }
    )