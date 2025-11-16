from enum import Enum

class ModelProvider(Enum):
    """Define los proveedores de LLM soportados."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"

class OpenAIModels(Enum):
    """Define los nombres de los modelos específicos de OpenAI."""
    GPT_4O = "gpt-4o"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4_1_MINI = "gpt-4.1-mini"
