from typing import TypedDict


class GeneralInformationState(TypedDict):
    question: str = ""
    response: str = ""
    context: dict = {}  # Changed to dict to match usage
    general_information_agent: str = ""  # Store spent agent response

class ReportState(TypedDict):
    question: str = ""
    response: str = ""
    context: dict = {}  # Changed to dict to match usage
    spent_response: str = ""  # Store spent agent response
    industry_response: str = ""  # Store industry agent response
    regimen_response: str = ""  # Store regimen agent response
    sectors_response: str = ""  # Store sectors agent response
    growth_interanual_response: str = ""  # Store growth_interanual agent response