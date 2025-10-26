#!/usr/bin/env python3
"""
LangGraph application with a simple greeting node.
"""

import os
from typing import Dict, Any
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure LangSmith if API key is provided
if os.getenv("LANGSMITH_API_KEY"):
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "langgraph-greeting-app")
    print(f"🔍 LangSmith tracing enabled for project: {os.environ['LANGCHAIN_PROJECT']}")
else:
    print("ℹ️  LangSmith not configured. Set LANGSMITH_API_KEY and LANGSMITH_PROJECT to enable tracing.")


# Define AgentState as a simple dict structure
class AgentState(TypedDict):
    message: str


def greeting_node(state: AgentState) -> AgentState:
    """Simple node that adds a greeting message to the state"""
    
    state['message'] = "Hey " + state["message"] + ", how is your day going?"
    
    return state


def create_graph():
    """Create and configure the LangGraph"""
    
    # Initialize the StateGraph
    workflow = StateGraph(AgentState)
    
    # Add the greeting node
    workflow.add_node("greeting", greeting_node)
    
    # Define the graph flow
    workflow.add_edge(START, "greeting")
    workflow.add_edge("greeting", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app


def main():
    """Main function to test the graph"""
    
    # Create the graph
    app = create_graph()
    
    # Test with sample input
    initial_state = {"message": "Alice"}
    
    print("Initial state:", initial_state)
    
    # Run the graph
    result = app.invoke(initial_state)
    
    print("Final output :", result)


if __name__ == "__main__":
    main()
