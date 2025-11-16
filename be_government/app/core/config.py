# config/config.py

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

DEFAULT_PIB_COLUMN = os.getenv("DEFAULT_PIB_COLUMN", "PIB_SD")
ADMINISTRATION_PERIOD_YEARS = int(os.getenv("ADMINISTRATION_PERIOD_YEARS", 4))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TOKEN_LIMIT = int(os.getenv("TOKEN_LIMIT", 4096))
SPENT_DATA_RELATIVE_PATH = os.getenv("SPENT_DATA_RELATIVE_PATH", "data/datasets/pib_yoy_componentes_gasto.txt")

