import os
from enum import Enum
from typing import Optional, Dict, Any, List
from langchain_core.messages import (
    BaseMessage, 
)
from abc import ABC, abstractmethod
from app.models.enums.ai_model_enums import ModelProvider
# --- 1. Interfaz (Contrato del Producto) ---
# Definir una interfaz (Clase Base Abstracta) es una buena práctica 
# para el Patrón de Fábrica. Asegura que cualquier cliente que 
# creemos (OpenAI, Anthropic, etc.) tenga los mismos métodos.

class LLMClient(ABC):
    """
    Define la interfaz común (contrato) que todos los clientes LLM 
    deben implementar.
    """
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """Genera una respuesta basada en un prompt."""
        pass

    @abstractmethod
    def generate_chat_response(self, messages: List[BaseMessage] ) -> str | list[str | dict]:
        """Genera una respuesta basada en varios  prompts."""
        pass
        


# --- 2. Fábrica (El Creador) ---
class LLMClientFactory:
    """
    Fábrica para crear instancias de clientes LLM específicos.
    Utiliza importación dinámica (lazy loading) para evitar cargar 
    dependencias innecesarias si no se usan.
    """

    @staticmethod
    def create_client(
        provider: ModelProvider, 
        config: Optional[Dict[str, Any]] = None
    ) -> LLMClient:
        """
        Crea y devuelve un cliente LLM basado en el proveedor.

        Args:
            provider: El ModelProvider (ej. ModelProvider.OPENAI).
            config: Un diccionario opcional para sobreescribir la 
                    configuración por defecto del cliente.

        Returns:
            Una instancia de un cliente que cumple con la interfaz LLMClient.
        
        Raises:
            ValueError: Si el proveedor no está soportado.
        """
        
        if provider == ModelProvider.OPENAI:
            try:
                from openai_client import OpenAIClient
            except ImportError:
                from .openai_client import OpenAIClient                
            return OpenAIClient(config=config)
        
        elif provider == ModelProvider.GOOGLE:
            try:
                from gemini_client import GeminiClient
            except ImportError:
                # Maneja el caso donde el archivo se ejecuta directamente
                from .gemini_client import GeminiClient                
            return GeminiClient(config=config)

        # --- Punto de Extensión ---
        # Si quisieras añadir Anthropic, solo crearías 'anthropic_client.py'
        # y añadirías la lógica aquí:
        #
        # elif provider == ModelProvider.ANTHROPIC:
        #     from .anthropic_client import AnthropicClient
        #     return AnthropicClient(config=config)
        #
        
        else:
            # Error si el proveedor no está implementado en la fábrica
            raise ValueError(f"Proveedor de LLM no soportado: {provider.name}")
