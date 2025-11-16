import os
from app.clients.llm_client import LLMClientFactory
from app.models.enums.ai_model_enums import ModelProvider
from app.pipelines.report_pipeline import ReportPipeline
from app.services.data_load_service import DataLoadService
from app.core.config import INDUSTRY_DATA_RELATIVE_PATH, INTERANUAL_GROWTH_DATA_RELATIVE_PATH, REGIMEN_DATA_RELATIVE_PATH, SECTORS_DATA_RELATIVE_PATH, SPENT_DATA_RELATIVE_PATH


class ChatService:
    def __init__(self):
        self.report_pipeline = ReportPipeline()
        self.data_load_service = DataLoadService()

    def report_generation(self, question):
        print("--- 1. Iniciando generación de reporte ---")
        try:
            # Load the context data using the DataLoadService with the relative path from config
            context_data = {}
            context_spent_data = self.data_load_service.load_data(SPENT_DATA_RELATIVE_PATH)
            context_industry_data = self.data_load_service.load_data(INDUSTRY_DATA_RELATIVE_PATH)
            context_regimen_data = self.data_load_service.load_data(REGIMEN_DATA_RELATIVE_PATH)
            context_sectors_data = self.data_load_service.load_data(SECTORS_DATA_RELATIVE_PATH)
            context_interannual_growth_data = self.data_load_service.load_data(INTERANUAL_GROWTH_DATA_RELATIVE_PATH)
            ###### TODO Agregar aqui el contexto de los otros agentes ######
            context_data["spent"] = context_spent_data
            context_data["industry"] = context_industry_data
            context_data["regimen"] = context_regimen_data
            context_data["sectors"] = context_sectors_data
            context_data["growth_interanual"] = context_interannual_growth_data

            # Pass the loaded context data to the report pipeline
            response = self.report_pipeline.run(question, context=context_data)
            print(f"Respuesta del pipeline: {response}\n")
            return f"{response}\n"
        except Exception as e:
            print(f"Error en la generación del reporte: {e}\n")
            raise e

        