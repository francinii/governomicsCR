from typing import TypedDict
from langgraph.graph import StateGraph, END
from app.agents.general_information_agents import GeneralInformationAgent
from app.models.states_langraph_models import GeneralInformationState

class GeneralInformationPipeline:
    def __init__(self):
        self.general_information_agent = GeneralInformationAgent()
        workflow = StateGraph(GeneralInformationState)
        # Use lambda to capture which agent to use for each node
        workflow.add_node("agent_general_information_node", lambda state: self._call_agent(state, "agent_general_information_node"))
        workflow.add_node("start", lambda state: state)
        workflow.set_entry_point("start")
        workflow.add_edge("start", "agent_general_information_node")
        workflow.add_edge("agent_general_information_node", END)
        self.app = workflow.compile()

    def _call_agent(self, state: GeneralInformationState, agent_type: str):
        """
        Generic method to call the appropriate agent based on agent_type.
        This keeps the pattern of a single _call_agent method while being scalable.
        """
        print(f"--- Agente de Reporte ({agent_type}) en ejecución (Langgraph) ---")
        question = state["question"]
        context = state["context"]
        general_information_agent_context = context.get("general_information_agent", "")
        response = self.general_information_agent.run(question, context=general_information_agent_context)
        return {"response": response}      

    def run(self, question: str, context: dict = {}): # Add context parameter here
        print("--- Pipeline de Reporte en ejecución (Langgraph) ---")
        initial_state = GeneralInformationState(question=question, context=context)
        final_state = self.app.invoke(initial_state)
        return final_state["response"]
