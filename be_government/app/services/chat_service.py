import os
from app.clients.llm_client import LLMClientFactory
from app.models.enums.ai_model_enums import ModelProvider
from app.pipelines.report_pipeline import ReportPipeline
from app.services.data_load_service import DataLoadService
from app.core.config import SPENT_DATA_RELATIVE_PATH


class ChatService:
    def __init__(self):
        self.report_pipeline = ReportPipeline()
        self.data_load_service = DataLoadService()

    def report_generation(self, question):
        print("--- 1. Iniciando generación de reporte ---")
        try:
            # Load the context data using the DataLoadService with the relative path from config
            context_data = self.data_load_service.load_data(SPENT_DATA_RELATIVE_PATH)
            ###### TODO Agregar aqui el contexto de los otros agentes ######

            # Pass the loaded context data to the report pipeline
            response = self.report_pipeline.run(question, context=context_data)
            print(f"Respuesta del pipeline: {response}\n")
            return f"{response}\n"
        except Exception as e:
            print(f"Error en la generación del reporte: {e}\n")
            raise e

        