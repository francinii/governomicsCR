from enum import Enum

class AgentType(Enum):
    """Define los tipos de agentes de IA soportados."""
    GENERAL_INFORMATION = "general_information"
    REPORTING = "reporting"
    DATA_ANALYSIS = "data_analysis"
    SPENT = "spent"
    INDUSTRY = "industry"
    REGIMEN = "regimen"
    SECTORS = "sectors"
    GROWTH_INTERANUAL = "growth_interanual"
    COMPLETED = "completed"
