# config/config.py

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

DEFAULT_PIB_COLUMN = os.getenv("DEFAULT_PIB_COLUMN", "PIB_SD")
ADMINISTRATION_PERIOD_YEARS = int(os.getenv("ADMINISTRATION_PERIOD_YEARS", 4))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print(f"DEBUG: GROQ_API_KEY loaded: {GROQ_API_KEY}") # Temporary debug line

