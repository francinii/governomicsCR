# gemini_client.py
import os
from typing import Optional, Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    HumanMessage, 
    BaseMessage, 
    SystemMessage, 
    AIMessage
)
from app.clients.llm_client import LLMClient
from app.models.enums.ai_model_enums import GeminiModels
from app.core.config import TOKEN_LIMIT

class GeminiClient(LLMClient):
    """
    Cliente específico (Producto Concreto) que usa LangChain para interactuar
    con la API de Google Gemini. Implementa la interfaz LLMClient.
    """
    
    # El cliente de LangChain se almacena aquí
    client: ChatGoogleGenerativeAI
    # Almacenamos la clave de API por separado para nuestras propias verificaciones
    api_key: Optional[str]
    _model_name: str  # Almacenar el nombre del modelo
    
    @staticmethod
    def list_available_models(api_key: Optional[str] = None) -> List[str]:
        """
        Lista los modelos de Gemini disponibles para la API key proporcionada.
        
        Args:
            api_key: La API key de Google. Si no se proporciona, usa la variable de entorno.
            
        Returns:
            Lista de nombres de modelos disponibles.
        """        
        try:
            if not api_key:
                api_key = os.getenv("GOOGLE_API_KEY")
            
            if not api_key:
                print("⚠️  No se proporcionó API key")
                return []
            
            genai.configure(api_key=api_key)
            models = genai.list_models()
            
            available_models = []
            for model in models:
                # Solo modelos que soportan generateContent
                if 'generateContent' in model.supported_generation_methods:
                    available_models.append(model.name.replace('models/', ''))
            
            print(f"✅ Modelos disponibles ({len(available_models)}):")
            for model in available_models:
                print(f"   - {model}")
            
            return available_models
        except Exception as e:
            print(f"❌ Error al listar modelos: {e}")
            return []

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa el cliente de Gemini usando LangChain.
        """
        
        # 1. Establecer valores por defecto para los parámetros de ChatGoogleGenerativeAI
        # Usar gemini-pro como modelo por defecto (más compatible)
        client_params = {
            "google_api_key": os.getenv("GOOGLE_API_KEY"),
            "model": GeminiModels.GEMINI_PRO.value,  # Modelo legacy más compatible
            "temperature": 0.7,  # Un default razonable
            "max_output_tokens": TOKEN_LIMIT,
            "timeout": 220,
        }

        # Almacena el nombre del modelo que se está utilizando
        self._model_name = client_params["model"]

        # 2. Almacena la clave de API en el atributo de la clase
        # Usamos .get() para evitar un error si 'google_api_key' no está
        self.api_key = client_params.get("google_api_key") 

        if not self.api_key:
            print(f"ADVERTENCIA: La variable de entorno 'GOOGLE_API_KEY' no está configurada.")

        # 3. Aplicar configuración personalizada (si existe)
        if config:
            client_params.update(config)
            # Si la config sobreescribe la google_api_key, actualiza nuestro atributo
            if "google_api_key" in config:
                self.api_key = config["google_api_key"]
            # Actualizar el nombre del modelo si se proporciona
            if "model" in config:
                self._model_name = config["model"]

        # 4. Filtra parámetros None antes de pasarlos a ChatGoogleGenerativeAI
        final_client_params = {k: v for k, v in client_params.items() if v is not None}

        try:
            # 5. Inicializar el cliente de LangChain
            self.client = ChatGoogleGenerativeAI(**final_client_params)
            print(f"✅ Cliente Gemini inicializado con modelo: {self._model_name}")
        except Exception as e:
            print(f"❌ Error al inicializar ChatGoogleGenerativeAI: {e}")
            print(f"💡 Verifica que:")
            print(f"   1. Tu API key de Google es válida")
            print(f"   2. El modelo '{self._model_name}' está disponible en tu región")
            print(f"   3. Tienes permisos para usar este modelo")
            
            # Intentar listar modelos disponibles si hay un error 404
            if "404" in str(e) or "not found" in str(e).lower():
                print(f"\n🔍 Intentando listar modelos disponibles...")
                available_models = self.list_available_models(self.api_key)
                if available_models:
                    print(f"\n💡 Modelos disponibles encontrados. Intenta usar uno de estos:")
                    for model in available_models[:5]:  # Mostrar solo los primeros 5
                        print(f"   - {model}")
                    print(f"\n   Puedes configurarlo así:")
                    print(f"   GeminiClient(config={{'model': '{available_models[0] if available_models else 'modelo-disponible'}'}})")
            
            raise

    def generate_response(self, prompt: str) -> str:
        """
        Genera una respuesta de Gemini usando el cliente de LangChain.
        """
        
        # Verificación de API key
        if not self.api_key:
            error_msg = "Error: Falta la API key de Google. No se puede conectar."
            print(error_msg)
            return error_msg
        
        messages: List[BaseMessage] = [HumanMessage(content=prompt)]

        try:
            print(f"\n[LangChain GeminiClient]: Conectando a {self._model_name}...")
            print(f"  Enviando Prompt: '{prompt[:60]}...'")

            response: BaseMessage = self.client.invoke(messages)
            
            # Debug: información detallada de la respuesta
            print(f"  🔍 DEBUG - Tipo de respuesta: {type(response)}")
            print(f"  🔍 DEBUG - Es AIMessage: {isinstance(response, AIMessage)}")
            
            if isinstance(response, AIMessage):
                content = response.content
                print(f"  🔍 DEBUG - Tipo de content: {type(content)}")
                print(f"  🔍 DEBUG - Content value: {repr(content)[:200]}")  # Primeros 200 caracteres
                print(f"  🔍 DEBUG - Content length: {len(str(content)) if content else 0}")
                
                # Verificar metadatos adicionales de la respuesta
                if hasattr(response, 'response_metadata'):
                    print(f"  🔍 DEBUG - response_metadata: {response.response_metadata}")
                if hasattr(response, 'usage_metadata'):
                    print(f"  🔍 DEBUG - usage_metadata: {response.usage_metadata}")
                if hasattr(response, 'additional_kwargs'):
                    print(f"  🔍 DEBUG - additional_kwargs: {response.additional_kwargs}")
                
                # Listar todos los atributos disponibles
                print(f"  🔍 DEBUG - Atributos disponibles: {[attr for attr in dir(response) if not attr.startswith('_')]}")
                
                # Si content es None, intentar otros atributos
                if content is None:
                    print("  ⚠️  Content es None, buscando otros atributos...")
                    # Intentar acceder a otros atributos comunes
                    if hasattr(response, 'text'):
                        content = response.text
                        print(f"  🔍 DEBUG - Usando response.text: {len(str(content)) if content else 0}")
                    elif hasattr(response, 'message'):
                        content = response.message
                        print(f"  🔍 DEBUG - Usando response.message: {len(str(content)) if content else 0}")
                
                # Verificar si el contenido está vacío
                if not content or (isinstance(content, str) and len(content.strip()) == 0):
                    print("⚠️  ADVERTENCIA: La respuesta de Gemini está vacía")
                    print(f"  🔍 DEBUG - Content completo: {repr(content)}")
                    print(f"  ⚠️  Posibles causas:")
                    print(f"     1. El modelo '{self._model_name}' podría no existir o no estar disponible")
                    print(f"     2. El prompt podría estar causando que el modelo no responda")
                    print(f"     3. Podría haber un bloqueo de seguridad del modelo")
                    print(f"  💡 Sugerencia: Intenta cambiar el modelo a 'gemini-1.5-flash' o 'gemini-1.5-pro'")
                    return "Error: La respuesta del modelo está vacía."
                
                # Si content es una lista, extraer el texto
                if isinstance(content, list):
                    print(f"  🔍 DEBUG - Content es una lista con {len(content)} elementos")
                    text_parts = []
                    for i, item in enumerate(content):
                        print(f"  🔍 DEBUG - Item {i}: tipo={type(item)}, valor={repr(str(item)[:50])}")
                        if isinstance(item, dict):
                            text_parts.append(item.get('text', str(item)))
                        elif isinstance(item, str):
                            text_parts.append(item)
                        else:
                            text_parts.append(str(item))
                    content = '\n'.join(text_parts)
                    print(f"  🔍 DEBUG - Content después de procesar lista: {len(content)} caracteres")
                
                result = content if isinstance(content, str) else str(content)
                print(f"  ✅ Respuesta final: {len(result)} caracteres")
                return result
            else:
                print(f"  ⚠️  Respuesta no es AIMessage, tipo: {type(response)}")
                result = str(response)
                print(f"  ✅ Respuesta convertida a string: {len(result)} caracteres")
                return result

        except Exception as e:
            error_msg = f"Error durante la llamada a LangChain: {e}"
            print(f"  ❌ ERROR: {error_msg}")
            print(f"  🔍 DEBUG - Tipo de excepción: {type(e).__name__}")
            print(f"  🔍 DEBUG - Detalles del error: {str(e)}")
            
            # Detectar errores específicos de modelo no encontrado
            if "404" in str(e) and "not found" in str(e).lower():
                print(f"  ⚠️  El modelo '{self._model_name}' no está disponible")
                print(f"  💡 Sugerencias:")
                print(f"     1. Verifica que tu API key tenga acceso a este modelo")
                print(f"     2. Intenta usar 'gemini-pro' (modelo legacy más compatible)")
                print(f"     3. Verifica los modelos disponibles en: https://ai.google.dev/models")
                print(f"     4. Puedes configurar el modelo en la inicialización del cliente")
            
            import traceback
            print(f"  🔍 DEBUG - Traceback: {traceback.format_exc()}")
            return error_msg
            
    def generate_chat_response(self, messages: List[BaseMessage]) -> str:
        """
        Genera una respuesta de chat más compleja.
        """
        # Verificación de API key
        if not self.api_key:
            return "Error: Falta la API key de Google."
            
        try:
            print(f"\n[LangChain GeminiClient]: Conectando a {self._model_name}...")
            print(f"  Enviando {len(messages)} mensajes...")          
            response: BaseMessage = self.client.invoke(messages)
            
            # Debug: imprimir tipo de respuesta
            print(f"  Tipo de respuesta: {type(response)}")
            
            if isinstance(response, AIMessage):
                content = response.content
                print(f"  Contenido extraído: {len(content) if content else 0} caracteres")
                
                # Verificar si el contenido está vacío o es solo whitespace
                if not content or (isinstance(content, str) and len(content.strip()) == 0):
                    print("⚠️  ADVERTENCIA: La respuesta de Gemini está vacía o solo contiene whitespace")
                    return "Error: La respuesta del modelo está vacía."
                
                # Si content es una lista (algunos modelos devuelven listas), extraer el texto
                if isinstance(content, list):
                    print(f"  Contenido es una lista con {len(content)} elementos")
                    # Intentar extraer texto de la lista
                    text_parts = []
                    for item in content:
                        if isinstance(item, dict):
                            text_parts.append(item.get('text', str(item)))
                        elif isinstance(item, str):
                            text_parts.append(item)
                        else:
                            text_parts.append(str(item))
                    content = '\n'.join(text_parts)
                    print(f"  Contenido extraído de lista: {len(content)} caracteres")
                
                return content if isinstance(content, str) else str(content)
            else:
                print(f"  Respuesta no es AIMessage, convirtiendo a string")
                return str(response)
        
        except Exception as e:
            error_msg = f"Error durante la llamada a LangChain: {e}"
            print(f"  ❌ {error_msg}")
            return error_msg

