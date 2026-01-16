import os
from dotenv import load_dotenv
from google import genai

# Load .env
load_dotenv()

# Create client with API key from env
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# Call Gemini
response = client.models.generate_content(
    model="models/gemini-flash-latest",
    contents="Say hello in one simple sentence"
)

print(response.text)
