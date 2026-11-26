from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    message: str


def greeting_node(state: AgentState):
    print("Hello from Greeting Node")
    return state


def uppercase_node(state: AgentState):
    state["message"] = state["message"].upper()
    return state


def print_node(state: AgentState):
    print(state["message"])
    return state


graph = StateGraph(AgentState)

graph.add_node("greeting", greeting_node)
graph.add_node("uppercase", uppercase_node)
graph.add_node("print", print_node)

graph.add_edge(START, "greeting")
graph.add_edge("greeting", "uppercase")
graph.add_edge("uppercase", "print")
graph.add_edge("print", END)

app = graph.compile()

app.invoke(
    {
        "message": "hello langgraph"
    }
)