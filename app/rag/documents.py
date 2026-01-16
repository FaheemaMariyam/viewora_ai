#Converts property database records into AI-readable documents
from langchain_core.documents import Document

def property_to_document(property_data: dict) -> Document:
    content = f"""
    Property Type: {property_data.get('type')}
    City: {property_data.get('city')}
    Locality: {property_data.get('locality')}
    Price Range: {property_data.get('price_range')}
    Area Size: {property_data.get('area_size')}
    Amenities: {', '.join(property_data.get('amenities', []))}
    """

    return Document(
        page_content=content.strip(),
        metadata={
            "property_id": property_data.get("id"),
            "city": property_data.get("city"),
            "locality": property_data.get("locality"),
            "type": property_data.get("type"),
        }
    )
