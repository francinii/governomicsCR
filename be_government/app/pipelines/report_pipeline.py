from langgraph.graph import StateGraph, END
from app.agents.report_agents import ReportCompletedAgent, ReportGrowthInteranualAgent, ReportRegimenAgent, ReportSectorsAgent, ReportSpentAgent, ReportIndustryAgent
from app.models.enums.ai_agent_enums import AgentType
from app.models.states_langraph_models import ReportState

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

        # Mapeo de agentes y claves de respuesta
        agent_map = [
            (AgentType.SPENT.value, self.report_spent_agent, "spent_response"),
            (AgentType.INDUSTRY.value, self.report_industry_agent, "industry_response"),
            (AgentType.REGIMEN.value, self.report_regimen_agent, "regimen_response"),
            (AgentType.SECTORS.value, self.report_sectors_agent, "sectors_response"),
            (AgentType.GROWTH_INTERANUAL.value, self.report_growth_interanual_agent, "growth_interanual_response"),
        ]

        for key, agent, response_key in agent_map:
            if agent_type == key:
                agent_context = context.get(key, "")
                response = agent.run(question, context=agent_context)
                return {response_key: response}

        if agent_type == AgentType.COMPLETED.value:  
            responses = []
            for key, agent, response_key in agent_map:   
                responses.append(state.get(response_key, ""))     
            for report in agent_map:
                print(f"REPORTE DE {report[0]}: {state.get(report[2], '')}")
            
            reports = {
                "gasto": responses[0],
                "industria": responses[1],
                "regimen": responses[2],
                "sectors": responses[3],
                "growth_interanual": responses[4]
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
        initial_state = ReportState(question=question,context=context)
        final_state = self.app.invoke(initial_state)
        return final_state["response"]
