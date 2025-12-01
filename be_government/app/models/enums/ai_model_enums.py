from enum import Enum

class ModelProvider(Enum):
    """Define los proveedores de LLM soportados."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"

class OpenAIModels(Enum):
    """
    Define los nombres de los modelos específicos de OpenAI
    usados para generación de texto.
    """
    GPT_CURRENT_USE = "gpt-4.1-mini"
    # --- Familia GPT-5 ---    
    GPT_5_1 = "gpt-5.1"
    GPT_5_1_CHAT_LATEST = "gpt-5.1-chat-latest"
    GPT_5_1_CODEX = "gpt-5.1-codex"
    GPT_5_1_CODEX_MINI = "gpt-5.1-codex-mini"
    GPT_5_MINI = "gpt-5-mini"
    GPT_5_MINI_20250807 = "gpt-5-mini-2025-08-07"
    GPT_5 = "gpt-5"
    GPT_5_20250807 = "gpt-5-2025-08-07"
    GPT_5_PRO = "gpt-5-pro"
    GPT_5_PRO_20251006 = "gpt-5-pro-2025-10-06"
    
    # --- Familia GPT-4.1 ---
    GPT_4_1 = "gpt-4.1"
    GPT_4_1_MINI = "gpt-4.1-mini"
    GPT_4_1_NANO = "gpt-4.1-nano"

    # --- Familia GPT-4o ---
    GPT_4O = "gpt-4o"
    GPT_3_5_TURBO = "gpt-3.5-turbo"





class GeminiModels(Enum):
    """
    Define los nombres de los modelos específicos de Google Gemini.
    Nota: Los modelos con sufijo -latest pueden no estar disponibles en todas las regiones.
    """
    GEMINI_2_5_FLASH ="gemini-2.5-flash"
    # --- Familia Gemini 2.0 (Experimental) ---
    # GEMINI_2_0_FLASH = "gemini-2.0-flash-exp"  # Puede no estar disponible
    # GEMINI_2_0_FLASH_THINKING = "gemini-2.0-flash-thinking-exp"  # Puede no estar disponible
    
    # --- Familia Gemini 1.5 (Modelos estables) ---
    GEMINI_1_5_PRO = "gemini-1.5-pro"
    GEMINI_1_5_FLASH = "gemini-1.5-flash"  # Modelo por defecto recomendado
    
    # --- Familia Gemini 1.0 (Legacy) ---
    GEMINI_PRO = "gemini-pro"
    GEMINI_PRO_VISION = "gemini-pro-vision"