from typing import TypedDict
from langgraph.graph import StateGraph, END
from app.agents.report_agents import ReportCompletedAgent, ReportGrowthInteranualAgent, ReportRegimenAgent, ReportSectorsAgent, ReportSpentAgent, ReportIndustryAgent


class ReportState(TypedDict):
    question: str
    response: str
    context: dict  # Changed to dict to match usage
    spent_response: str  # Store spent agent response
    industry_response: str  # Store industry agent response
    regimen_response: str  # Store regimen agent response
    sectors_response: str  # Store sectors agent response
    growth_interanual_response: str  # Store growth_interanual agent response


class ReportPipeline:
    def __init__(self):
        self.report_spent_agent = ReportSpentAgent()
        self.report_industry_agent = ReportIndustryAgent()
        self.report_regimen_agent = ReportRegimenAgent()
        self.report_sectors_agent = ReportSectorsAgent()
        self.report_growth_interanual_agent = ReportGrowthInteranualAgent()
        self.complete_agent = ReportCompletedAgent()

        workflow = StateGraph(ReportState)
        # Use lambda to capture which agent to use for each node
        workflow.add_node("agent_spent_node", lambda state: self._call_agent(state, "spent"))
        workflow.add_node("agent_industry_node", lambda state: self._call_agent(state, "industry"))
        workflow.add_node("agent_regimen_node", lambda state: self._call_agent(state, "regimen"))
        workflow.add_node("agent_sectors_node", lambda state: self._call_agent(state, "sectors"))
        workflow.add_node("agent_growth_interanual_node", lambda state: self._call_agent(state, "growth_interanual"))
        workflow.add_node("agent_completed_node", lambda state: self._call_agent(state, "completed"))


        workflow.add_node("start", lambda state: state)
        workflow.set_entry_point("start")
        # Agents execute in parallel from start
        workflow.add_edge("start", "agent_spent_node")
        workflow.add_edge("start", "agent_industry_node")
        workflow.add_edge("start", "agent_regimen_node")
        workflow.add_edge("start", "agent_sectors_node")
        workflow.add_edge("start", "agent_growth_interanual_node")

        workflow.add_edge("agent_spent_node", "agent_completed_node")
        workflow.add_edge("agent_industry_node", "agent_completed_node")
        workflow.add_edge("agent_regimen_node", "agent_completed_node")
        workflow.add_edge("agent_sectors_node", "agent_completed_node")
        workflow.add_edge("agent_growth_interanual_node", "agent_completed_node")

        workflow.add_edge("agent_completed_node", END)
        self.app = workflow.compile()

    def _call_agent(self, state: ReportState, agent_type: str):
        """
        Generic method to call the appropriate agent based on agent_type.
        This keeps the pattern of a single _call_agent method while being scalable.
        """
        print(f"--- Agente de Reporte ({agent_type}) en ejecución (Langgraph) ---")
        question = state["question"]
        context = state.get("context", {})

        if agent_type == "spent":
            spent_context = context.get("spent", "")
            response = self.report_spent_agent.run(question, context=spent_context)
            #response = '......... Comentado por cuestiones monetarias .........'
            return {"spent_response": response}

        elif agent_type == "industry":
            industry_context = context.get("industry", "")
            response = self.report_industry_agent.run(question, context=industry_context)
            #response = '......... Comentado por cuestiones monetarias .........'
            return {"industry_response": response}

        elif agent_type == "regimen":
            regimen_context = context.get("regimen", "")
            response = self.report_regimen_agent.run(question, context=regimen_context)
            #response = '......... Comentado por cuestiones monetarias .........'
            return {"regimen_response": response}

        elif agent_type == "sectors":
            sectors_context = context.get("sectors", "")
            response = self.report_sectors_agent.run(question, context=sectors_context)
            #response = '......... Comentado por cuestiones monetarias .........'
            return {"sectors_response": response}

        elif agent_type == "growth_interanual":
            growth_interanual_context = context.get("growth_interanual", "")
            response = self.report_growth_interanual_agent.run(question, context=growth_interanual_context)
            #response = '......... Comentado por cuestiones monetarias .........'
            return {"growth_interanual_response": response}

        elif agent_type == "completed":
            # Obtener todas las respuestas de los agentes
            spent_response = state.get("spent_response", "")
            industry_response = state.get("industry_response", "")
            regimen_response = state.get("regimen_response", "")
            sectors_response = state.get("sectors_response", "")
            growth_interanual_response = state.get("growth_interanual_response", "")


            print("------- REPORTES GENERADOS -----------")
            print("----------  REPORTE DE GASTO -----------")
            print(spent_response)
            print("----------  REPORTE DE INDUSTRIA -----------")
            print(industry_response)
            print("----------  REPORTE DE SECTORES -----------")
            print(sectors_response)
            print("----------  REPORTE DE REGIMEN -----------")
            print(regimen_response)
            print("----------  REPORTE DE CRECIMIENTO -----------")
            print(growth_interanual_response)
            
            # Construir el diccionario de reports con las claves que espera el agente completado
            reports = {
                "gasto": spent_response,
                "industria": industry_response,
                "regimen": regimen_response,
                "sectors": sectors_response,
                "growth_interanual": growth_interanual_response
            }
            response = self.complete_agent.run(user_question=question, 
                                                csv_context_data='', 
                                                reports=reports)            
            # Combinar todos los contextos CSV para metadatos            
            context = state.get("context", {})
            print("------- REPORTES FINAL GENERADO -----------")
            print(response)
            return {"response": response}
        else:
            return {"response": ""}

    def run(self, question: str, context: dict = {}): # Add context parameter here
        print("--- Pipeline de Reporte en ejecución (Langgraph) ---")
        initial_state = {
            "question": question, 
            "response": "", 
            "context": context,
            "spent_response": "",
            "industry_response": "",
            "regimen_response": "",
            "sectors_response": "",
            "growth_interanual_response": "",            
        }
        final_state = self.app.invoke(initial_state)
        return final_state["response"]
