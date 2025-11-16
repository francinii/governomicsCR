# openai_client.py
import os
from typing import Optional, Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    HumanMessage, 
    BaseMessage, 
    SystemMessage, 
    AIMessage
)
from app.clients.llm_client import LLMClient
from app.models.enums.ai_model_enums import OpenAIModels
from app.core.config import TOKEN_LIMIT # Import TOKEN_LIMIT


class OpenAIClient(LLMClient):
    """
    Cliente específico (Producto Concreto) que usa LangChain para interactuar
    con la API de OpenAI. Implementa la interfaz LLMClient.
    """
    
    # El cliente de LangChain se almacena aquí
    client: ChatOpenAI
    # Almacenamos la clave de API por separado para nuestras propias verificaciones
    api_key: Optional[str]
    _model_name: str # Añadir esta línea para almacenar el nombre del modelo

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa el cliente de OpenAI usando LangChain.
        """
        
        # 1. Establecer valores por defecto para los parámetros de ChatOpenAI
        client_params = {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": OpenAIModels.GPT_CURRENT_USE.value,
            "timeout": 220,
            "temperature": 0.7,  # Un default razonable
            "max_tokens": TOKEN_LIMIT # Add max_tokens here
        }

        # Almacena el nombre del modelo que se está utilizando
        self._model_name = client_params["model"]

        # 2. Almacena la clave de API en el atributo de la clase
        # Usamos .get() para evitar un error si 'api_key' no está
        self.api_key = client_params.get("api_key") 

        if not self.api_key:
            print(f"ADVERTENCIA: La variable de entorno 'OPENAI_API_KEY' no está configurada.")

        # 3. Aplicar configuración personalizada (si existe)
        if config:
            client_params.update(config)
            # Si la config sobreescribe la api_key, actualiza nuestro atributo
            if "api_key" in config:
                self.api_key = config["api_key"]

        # 4. Filtra parámetros None antes de pasarlos a ChatOpenAI
        final_client_params = {k: v for k, v in client_params.items() if v is not None}

        try:
            # 5. Inicializar el cliente de LangChain
            self.client = ChatOpenAI(**final_client_params)
        except Exception as e:
            print(f"Error al inicializar ChatOpenAI: {e}")
            raise

    def generate_response(self, prompt: str) -> str:
        """
        Genera una respuesta de OpenAI usando el cliente de LangChain.
        """
        
        # AHORA LA VERIFICACIÓN FUNCIONA
        if not self.api_key:  # <-- CORREGIDO
            error_msg = "Error: Falta la API key de OpenAI. No se puede conectar."
            print(error_msg)
            return error_msg
        
        messages: List[BaseMessage] = [HumanMessage(content=prompt)]

        try:
            print(f"\n[LangChain OpenAIClient]: Conectando a {self._model_name}...") # Usar _model_name
            print(f"  Enviando Prompt: '{prompt[:60]}...'")

            response: BaseMessage = self.client.invoke(messages)
            
            if isinstance(response, AIMessage):
                return response.content
            else:
                return str(response)

        except Exception as e:
            error_msg = f"Error durante la llamada a LangChain: {e}"
            print(error_msg)
            return error_msg
            
    def generate_chat_response(self, messages: List[BaseMessage]) -> str:
        """
        Genera una respuesta de chat más compleja.
        """
        # AHORA LA VERIFICACIÓN FUNCIONA
        if not self.api_key:  # <-- CORREGIDO
            return "Error: Falta la API key de OpenAI."
            
        try:
            print(f"\n[LangChain OpenAIClient]: Conectando a {self._model_name}...") # Usar _model_name
            print(f"  Enviando {len(messages)} mensajes...")          
            response: BaseMessage = self.client.invoke(messages)          
            if isinstance(response, AIMessage):
                return response.content
            else:
                return str(response)
        
        except Exception as e:
            return f"Error durante la llamada a LangChain: {e}"