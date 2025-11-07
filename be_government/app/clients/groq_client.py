from pandasai_litellm.litellm import LiteLLM
from app.core.config import GROQ_API_KEY # Import GROQ_API_KEY from config

class GroqClient:
    """
    Client for interacting with the Groq API using LiteLLM.
    """
    def __init__(self):
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        """
        Initializes the LiteLLM client for Groq.
        """
        try:
            llm_instance = LiteLLM(
                model="groq/llama-3.3-70b-versatile",
                api_key=GROQ_API_KEY,
                api_base="https://api.groq.com/openai/v1",
                custom_llm_provider="groq"
            )
            return llm_instance
        except Exception as e:
            print(f"Error initializing Groq LLM: {e}. Ensure API key is valid.")
            # Depending on desired error handling, you might want to raise the exception
            # or return None/a default LLM.
            raise

    def get_llm(self):
        """
        Returns the initialized LLM instance.
        """
        return self.llm