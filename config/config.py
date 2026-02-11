import os
from dotenv import load_dotenv

# Load .env from the config folder
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

GROQ_API_KEY = os.getenv("GROQ_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_KEY")

# The phone number authorized to use the Kill Switch (e.g., +201xxxxxxxxx)
OWNER_PHONE_NUMBER = os.getenv("OWNER_PHONE_NUMBER") 
WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "my_secure_token")