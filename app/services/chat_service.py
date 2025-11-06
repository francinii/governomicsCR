from pandasai import SmartDataframe
from app.clients.groq_client import GroqClient
from app.prompts.question_prompt import QUESTION_PROMPT
from app.prompts.prompt_report import REPORT_PROMPT
from app.schemas.pib import create_pib_schema


class ChatService:
    def __init__(self, groq_client: GroqClient):
        self.llm = groq_client.get_llm()
        self.smart_dataframe = self._setup_smart_dataframe()

    def _setup_smart_dataframe(self):
        """Carga los datos y configura el SmartDataframe."""
        print("--- 🧠 Cargando DataFrames de Estadísticas por Gobierno... ---")

        df = create_pib_schema(self.llm)
                    
        if df is None:
            raise ValueError("No se pudo cargar ningún DataFrame para el análisis.")
            
        print("\n--- Inicializando SmartDataframe para el Chat... ---")
        # If create_pib_schema returns a SmartDataframe, use it directly
        if isinstance(df, SmartDataframe):
            sdf = df
        else: # If it returns a regular DataFrame, wrap it in SmartDataframe
            sdf = SmartDataframe(
                df,
                config={
                "llm": self.llm, 
                "verbose": True, 
                "enable_cache": False, 
                "save_charts_path": "charts"
                }
            )
        return sdf

    def process_chat_query(self, query: str):
        """Process a query using pandasai schemas."""
        if not self.smart_dataframe:
            raise ValueError("SmartDataframe no inicializado. Asegúrate de que los datos se cargaron correctamente.")
        
        print("--- 🤖 GROQ/PANDASAI RESPONDIENDO... ---")
        try:
            response = self.smart_dataframe.chat(query, output_type="string")
            return str(response)
        except Exception as e:
            print(f"\n[ERROR DE PANDASAI]: Ocurrió un error. Verifica la complejidad de la consulta. Error: {e}")
            raise


    def process_chat_report(self, query: str):
        """Genera un informe detallado basado en la consulta del usuario."""
        if not self.smart_dataframe:
            raise ValueError("SmartDataframe no inicializado. Asegúrate de que los datos se cargaron correctamente.")

        report_prompt_formatted = REPORT_PROMPT.format(query=query)
        
        print("--- 🤖 GROQ/PANDASAI GENERANDO REPORTE DETALLADO... ---")
        try:
            report_response = self.smart_dataframe.chat(report_prompt_formatted, output_type="string")
            return str(report_response)
        except Exception as e:
            print(f"\n[ERROR DE PANDASAI EN REPORTE]: Ocurrió un error al generar el reporte. Error: {e}")
            raise
