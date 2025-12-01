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


class BaseReportAgent(ABC):
    """
    Clase base abstracta para agentes de reporte.
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
    
    def run(self, input_question: str, context: str = "") -> str:
        """
        Método común para ejecutar el agente.
        Reemplaza el placeholder {{#context#}} en el prompt y genera la respuesta.
        """
        print(f"--- Agente de Reporte de {self.agent_name} en ejecución ---")
        print("="*40 + "\n")
        # Logging del contexto recibido
        #print(f"[LOG] Contexto recibido por el agente '{self.agent_name}':")
        if context:
            print(f"Longitud: {len(context)} caracteres")
            preview = context[:300] if len(context) > 300 else context
            print(f"Preview: {preview}")
        else:
            print("Sin contexto proporcionado.")
        print("="*40 + "\n")
        
        if context:
            # Replace the {{#context#}} placeholder in the system prompt
            system_prompt_with_context = self.system_prompt.replace("{{#context#}}", context)
        else:
            system_prompt_with_context = self.system_prompt
        
        full_prompt = f"{system_prompt_with_context}\n\nPregunta del usuario: {input_question}"
        response = self.llm_client.generate_response(full_prompt)
        return response


class ReportSpentAgent(BaseReportAgent):
    def _get_system_prompt(self) -> str:
        return SPENT_PROMPT

    def _get_agent_name(self) -> str:
        return "gasto"


class ReportIndustryAgent(BaseReportAgent):
    def _get_system_prompt(self) -> str:
        return INDUSTRY_PROMPT    

    def _get_agent_name(self) -> str:
        return "industria"


class ReportRegimenAgent(BaseReportAgent):
    def _get_system_prompt(self) -> str:
        return REGIMEN_PROMPT        
    def _get_agent_name(self) -> str:
        return "regimen"


class ReportSectorsAgent(BaseReportAgent):
    def _get_system_prompt(self) -> str:
        return SECTORS_PROMPT
        
    def _get_agent_name(self) -> str:
        return "sectors"


class ReportGrowthInteranualAgent(BaseReportAgent):
    def _get_system_prompt(self) -> str:
        return GROWTH_INTERANUAL_PROMPT
        
    def _get_agent_name(self) -> str:
        return "growth_interanual"



class ReportCompletedAgent:    
    def __init__(self):
        """
        Inicializa el agente ensamblador.
        
        Args:
            system_prompt: La plantilla de string para el SystemMessage (JOIN_REPORT_PROMPT).
            human_prompt_template: La plantilla de string para el HumanMessage 
                                     (HUMAN_JOIN_REPORT_PROMPT).
        """
        self.llm_client = LLMClientFactory.create_client(ModelProvider.OPENAI, config={"model":OpenAIModels.GPT_4_1.value})
        
        # 1. Almacenamos las plantillas recibidas
        self.system_prompt = SYSTEM_JOIN_REPORT_PROMPT
        self.human_prompt_template = HUMAN_JOIN_REPORT_PROMPT

    def run(self, 
            user_question: str, 
            csv_context_data: str | None, 
            reports: Dict[str, str]
           ) -> str:
        """
        Ejecuta el agente ensamblador.
        
        Args:
            user_question: La pregunta original del usuario.
            csv_context_data: El string de los CSV originales (para metadatos).
            reports: Un diccionario con los informes de los sub-agentes.
                     Ej: {"gasto": "...", "industria": "..."}
        """
        import time
        start_time = time.time()

        print("--- Agente de Reporte ensamblador en ejecución ---")

        # DEBUG: Mostrar qué reports se reciben
        print("\n" + "="*60)
        print("🔍 DEBUG: Reports recibidos en ReportCompletedAgent")
        print("="*60)
        for key, value in reports.items():
            print(f"  📋 {key}:")
            print(f"     Longitud: {len(value)} caracteres")
            if len(value) > 150:
                print(f"     Preview: {value[:150]}...")
            else:
                print(f"     Contenido: {value}")
        print("="*60 + "\n")

        # 2. PREPARAR LOS DATOS PARA EL TEMPLATE
        # Extrae los informes con un fallback para evitar errores
        report_gasto = reports.get('gasto', 'No se proporcionó informe de gasto.')
        report_industria = reports.get('industria', 'No se proporcionó informe de industria.')
        report_sectors = reports.get('sectors', 'No se proporcionó informe sectorial.')
        report_regimen = reports.get('regimen', 'No se proporcionó informe de régimen.')
        report_growth_interanual = reports.get('growth_interanual', 'No se proporcionó informe de crecimiento interanual.')

        print(f"📊 report_gasto: {len(report_gasto)} caracteres")
        print(f"📊 report_industria: {len(report_industria)} caracteres")
        print(f"📊 report_sectors: {len(report_sectors)} caracteres")
        print(f"📊 report_regimen: {len(report_regimen)} caracteres")
        print(f"📊 report_growth_interanual: {len(report_growth_interanual)} caracteres")
        print(f"📊 csv_context_data: {len(csv_context_data) if csv_context_data else 0} caracteres")

        # 3. FORMATEAR EL MENSAJE HUMANO
        # Rellena la plantilla `HUMAN_JOIN_REPORT_PROMPT` con los datos
        try:
            human_message_content = self.human_prompt_template.format(
                user_question=user_question,
                report_gasto=report_gasto,
                report_industria=report_industria,
                report_sectors=report_sectors,
                report_regimen=report_regimen,
                report_growth_interanual=report_growth_interanual,
                csv_context_data=csv_context_data or ''
            )
            print(f"✅ Template formateado correctamente: {len(human_message_content)} caracteres")
        except KeyError as e:
            print(f"❌ Error: Falta una clave en la plantilla HUMAN_JOIN_REPORT_PROMPT: {e}")
            return f"Error de configuración del agente: falta la clave {e}"

        # 4. CONSTRUIR LA LISTA DE MENSAJES
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=human_message_content)
        ]

        # 5. LLAMAR AL MÉTODO DE CHAT
        print("Generando informe final...")
        response = self.llm_client.generate_chat_response(messages)
        print(f"Informe final generado. Longitud: {len(response)} caracteres")

        end_time = time.time()
        elapsed = end_time - start_time
        print(f"⏱️ Tiempo total de ejecución del informe final: {elapsed:.2f} segundos")

        if not response or len(response.strip()) == 0:
            print("⚠️  ADVERTENCIA: La respuesta está vacía!")
        elif len(response) < 50:
            print(f"⚠️  ADVERTENCIA: La respuesta es muy corta: {response}")

        return response