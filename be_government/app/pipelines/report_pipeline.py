from typing import TypedDict
from langgraph.graph import StateGraph, END
from app.agents.report_agents import ReportSpentAgent


class ReportState(TypedDict):
    question: str
    response: str
    context: str # Add context to the state


class ReportPipeline:
    def __init__(self):
        self.report_spent_agent = ReportSpentAgent()

        workflow = StateGraph(ReportState)
        workflow.add_node("agent_spent_node", self._call_agent)
        ######### TODO Agregar aqui mas nodos ############
        workflow.set_entry_point("agent_spent_node")
        workflow.add_edge("agent_spent_node", END)
        self.app = workflow.compile()

    def _call_agent(self, state: ReportState):
        print("--- Agente de Reporte en ejecución (Langgraph) ---")
        question = state["question"]
        context = state["context"] # Retrieve context from state
        response = self.report_spent_agent.run(question, context=context) # Pass context to agent
        return {"response": response}

    def run(self, question: str, context: str = ""): # Add context parameter here
        print("--- Pipeline de Reporte en ejecución (Langgraph) ---")
        initial_state = {"question": question, "response": "", "context": context} # Initialize context in state
        final_state = self.app.invoke(initial_state)
        return final_state["response"]
