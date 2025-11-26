from abc import ABC, abstractmethod
from app.clients.llm_client import LLMClientFactory
from app.models.enums.ai_model_enums import ModelProvider, OpenAIModels
from app.prompts.spent_prompt import SPENT_PROMPT
from app.prompts.industry_prompt import INDUSTRY_PROMPT
from app.prompts.join_report_prompt import SYSTEM_JOIN_REPORT_PROMPT, HUMAN_JOIN_REPORT_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Dict

from app.prompts.growth_interanual_prompt import GROWTH_INTERANUAL_PROMPT
from app.prompts.regimen_prompt import REGIMEN_PROMPT
from app.prompts.sectors_prompt import SECTORS_PROMPT
from app.prompts.general_information_prompt import GENERAL_INFORMATION_PROMPT


class BaseGeneralInformationAgent(ABC):
    """
    Clase base abstracta para agentes de informacion general.
    Implementa el método run común y requiere que las subclases definan el system_prompt.
    """
    
    def __init__(self):
        self.llm_client = LLMClientFactory.create_client(ModelProvider.OPENAI)
        self.system_prompt = self._get_system_prompt()
        self.agent_name = self._get_agent_name()
    
    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Retorna el prompt del sistema para este agente. Debe ser implementado por las subclases."""
        pass
    
    @abstractmethod
    def _get_agent_name(self) -> str:
        """Retorna el nombre del agente para logging. Debe ser implementado por las subclases."""
        pass
    
    def run(self, input_question: str, context = "") -> str:
        """
        Método común para ejecutar el agente.
        Reemplaza el placeholder {{#context#}} en el prompt y genera la respuesta.
        Admite context como str o dict.
        """
        print(f"--- Agente de Reporte de {self.agent_name} en ejecución ---")
        print("="*40 + "\n")
        print("="*40 + "\n")

        # Si el contexto es dict, conviértelo a string legible
        if isinstance(context, dict):
            import json
            context_str = json.dumps(context, ensure_ascii=False, indent=2)
        else:
            context_str = str(context)

        if context_str:
            system_prompt_with_context = self.system_prompt.replace("{{#context#}}", context_str)
        else:
            system_prompt_with_context = self.system_prompt

        full_prompt = f"{system_prompt_with_context}\n\nPregunta del usuario: {input_question}"
        response = self.llm_client.generate_response(full_prompt)
        return response


class GeneralInformationAgent(BaseGeneralInformationAgent):
    def _get_system_prompt(self) -> str:
        return GENERAL_INFORMATION_PROMPT

    def _get_agent_name(self) -> str:
        return "general_information"

