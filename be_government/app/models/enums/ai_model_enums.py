from enum import Enum

class ModelProvider(Enum):
    """Define los proveedores de LLM soportados."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"


from enum import Enum

class OpenAIModels(Enum):
    """
    Define los nombres de los modelos específicos de OpenAI, 
    basado en la lista de API proporcionada.
    """
    
    # --- Familia GPT-5 ---
    GPT_5_1 = "gpt-5.1"
    GPT_5_MINI = "gpt-5-mini"
    GPT_5_NANO = "gpt-5-nano"
    
    # --- Familia GPT-4.1 ---
    GPT_4_1 = "gpt-4.1"
    GPT_4_1_MINI = "gpt-4.1-mini"
    GPT_4_1_MINI_EXTENDED = "gpt-4.1-mini-128k"    
    GPT_4_1_NANO = "gpt-4.1-nano"

    # --- Familia O3/O4 ---
    O3 = "o3"
    O4_MINI = "o4-mini"
    
    # --- Familia GPT-4o (Público) ---
    GPT_4O = "gpt-4o"