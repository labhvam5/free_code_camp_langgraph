#!/usr/bin/env python3
"""
LangGraph application with conditional routing for calculator operations.
"""

import os
from typing import Dict, Any
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
import random
from typing import Dict, List, TypedDict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure LangSmith if API key is provided
if os.getenv("LANGSMITH_API_KEY"):
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "langgraph-conditional-calculator")
    print(f"🔍 LangSmith tracing enabled for project: {os.environ['LANGCHAIN_PROJECT']}")
else:
    print("ℹ️  LangSmith not configured. Set LANGSMITH_API_KEY and LANGSMITH_PROJECT to enable tracing.")


# Define AgentState as a TypedDict structure
class AgentState(TypedDict):
    name: str
    number: List[int]
    counter: int


def greeting_node(state: AgentState) -> AgentState:
    """Greeting Node which says hi to the person"""
    state["name"] = f"Hi there, {state['name']}"
    state["counter"] = 0 

    return state

def random_node(state: AgentState) -> AgentState:
    """Generates a random number from 0 to 10"""
    state["number"].append(random.randint(0, 10))
    state["counter"] += 1

    return state


def should_continue(state: AgentState) -> AgentState:
    """Function to decide what to do next"""
    if state["counter"] < 5:
        print("ENTERING LOOP", state["counter"])
        return "loop"  # Continue looping
    else:
        return "exit"  # Exit the loop


def create_graph():
    """Create and configure the conditional LangGraph"""
    
    graph = StateGraph(AgentState)

    graph.add_node("greeting", greeting_node)
    graph.add_node("random", random_node)
    graph.add_edge("greeting", "random")


    graph.add_conditional_edges(
        "random",     # Source node
        should_continue, # Action
        {
            "loop": "random",  
            "exit": END          
        }
    )

    graph.set_entry_point("greeting")

    app = graph.compile()

    return app

def main():
    """Main function to test the conditional graph"""

    # Create the graph
    app = create_graph()

    result = app.invoke({"name": "Vaibhav", "number":[], "counter":-100})

    print("Final result:", result)


if __name__ == "__main__":
    main()
