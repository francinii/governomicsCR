
import pandasai as pai
#from pandasai.llm.openai import OpenAI
from pandasai_litellm.litellm import LiteLLM
import sys
import os

# Add the project root to sys.path to enable imports from config and utils
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from utils.data_loader import load_all_excel_data, assign_administration_period
from config.config import OPENAI_API_KEY, DEEPSEEK_API_KEY, GROQ_API_KEY

# Load and prepare data using the existing data_loader functions
combined_df = load_all_excel_data()
if combined_df is not None:
    combined_df = assign_administration_period(combined_df)

if combined_df is not None and not combined_df.empty:
    # Initialize OpenAI LLM
    #llm = OpenAI(api_token=OPENAI_API_KEY)
    
    #llm = LiteLLM(model="gpt-4.1-mini", api_key=OPENAI_API_KEY)
    #llm = LiteLLM(model="deepseek-chat", api_key=DEEPSEEK_API_KEY)
    '''llm = LiteLLM(
    model="deepseek-chat",
    api_key=DEEPSEEK_API_KEY,
    api_base="https://api.deepseek.com/v1",  # Endpoint oficial
    custom_llm_provider="deepseek"            # Necesario para LiteLLM
    )'''


    llm = LiteLLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
    api_base="https://api.groq.com/openai/v1",
    custom_llm_provider="groq"
    )

    # Configure PandasAI to use this LLM
    pai.config.set({
        "llm": llm
    })

    # Example query
    user_question = "What is the highest PIB_SD recorded across all administrations?"
    user_question = """
                    Generate a detailed analytical report of the PIB_SD variable across all administrations.
                    Include: 
                    - average, max, and min values per administration
                    - trends or notable changes over time
                    - possible interpretations of variations
                    - a short conclusion summarizing the main insights.
                    Present it in a clear, narrative format.
                    """
    print(f"User question for PandasAI: {user_question}")

    # Use PandasAI to chat with the DataFrame
    response = pai.SmartDataframe(combined_df).chat(user_question)
    print(f"PandasAI response: {response}")
else:
    print("No data loaded. Cannot proceed with PandasAI test.")
