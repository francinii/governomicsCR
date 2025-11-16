from app.clients.llm_client import LLMClientFactory
from app.models.enums.ai_model_enums import ModelProvider
from app.prompts.spent_prompt import SPENT_PROMPT

class ReportSpentAgent:
    def __init__(self):
        self.llm_client = LLMClientFactory.create_client(ModelProvider.OPENAI)
        self.system_prompt = SPENT_PROMPT

    def run(self, input_question: str, context: str = ""):  # Add context parameter
        print("--- Agente de Reporte en ejecución ---")
        if context:
            # Replace the {{#context#}} placeholder in the system prompt
            system_prompt_with_context = self.system_prompt.replace("{{#context#}}", context)
        else:
            system_prompt_with_context = self.system_prompt
            
        full_prompt = f"{system_prompt_with_context}\n\nPregunta del usuario: {input_question}"
        response = self.llm_client.generate_response(full_prompt)
        return response
