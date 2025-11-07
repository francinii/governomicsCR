# Define the graph
from langgraph.graph import StateGraph, START, END
from app.agents.pib_statistics_agent import statistics_agent


class State(TypeDict):
    history: str


def pib_report_pipeline(agent_func):
    """
    Build a simple graph
    agent_func: agent function that take and return a state.

    Return:
        StateGraph.
    """
    builder = StateGraph(State)
    builder.add_edge(START, 'statistic_agent')
    builder.add_node("statistic_agent", statistics_agent)
    builder.add_edge("statistic_agent", END)
    #builder.add_conditional_edges
    return builder.compile()
